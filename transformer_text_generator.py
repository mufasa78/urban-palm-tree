import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from deep_translator import GoogleTranslator
import pandas as pd

class TransformerTextGenerator:
    def __init__(self, model_name="distilgpt2"):
        """
        Initialize the transformer text generator with a pre-trained model.

        Args:
            model_name (str): The name of the pre-trained model to use
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.translator = GoogleTranslator(source='en', target='zh-CN')

        try:
            self.logger.info(f"Initializing transformer text generator with model: {model_name}")

            # Set device (use CUDA if available, otherwise CPU)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.logger.info(f"Using device: {self.device}")

            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

            # Set padding token for GPT-2 models which don't have one by default
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.model.to(self.device)

            self.logger.info("Transformer text generator initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize transformer text generator: {e}")
            raise

    def get_model_info(self):
        """Return information about the loaded model"""
        return {
            "model_name": self.model_name,
            "parameters": sum(p.numel() for p in self.model.parameters()),
            "device": self.device
        }

    def _prepare_topic_context(self, topic_data):
        """Prepare context from topic-specific data"""
        if topic_data is None:
            return ""
            
        context = []
        for col in topic_data.columns:
            texts = topic_data[col].dropna().astype(str).tolist()
            # Take a few random samples from the topic data
            samples = pd.Series(texts).sample(min(3, len(texts))).tolist()
            context.extend(samples)
        
        # Join the samples with newlines
        return "\n".join(context)

    def generate_text(self, prompt, max_length=200, temperature=0.7, topic_data=None):
        """
        Generate text based on the given prompt using the transformer model.

        Args:
            prompt (str): The input text to base generation on
            max_length (int): Maximum length of the generated text
            temperature (float): Controls randomness (higher = more random)
            topic_data (pd.DataFrame): Topic-specific data to provide context

        Returns:
            str: The generated text
        """
        try:
            self.logger.info(f"Generating text for prompt: {prompt}")

            # Translate Chinese prompt to English for the model
            try:
                en_prompt = GoogleTranslator(source='zh-CN', target='en').translate(prompt)
            except Exception as e:
                self.logger.warning(f"Translation failed, using original prompt: {e}")
                en_prompt = prompt

            # Prepare topic-specific context if available
            context = self._prepare_topic_context(topic_data)
            
            # Combine context with prompt if available
            full_prompt = f"{context}\n{en_prompt}" if context else en_prompt

            # Encode the input
            inputs = self.tokenizer(full_prompt, return_tensors="pt", truncation=True)
            if torch.cuda.is_available():
                inputs = inputs.to('cuda')

            # Generate text
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95
                )

            # Decode the generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Remove the context from the generated text if it was used
            if context:
                generated_text = generated_text.replace(context, "").strip()

            # Translate back to Chinese
            try:
                generated_text = self.translator.translate(generated_text)
            except Exception as e:
                self.logger.error(f"Translation error: {e}")
                # Continue with untranslated text if translation fails

            self.logger.info("Text generation successful")
            return generated_text

        except Exception as e:
            self.logger.error(f"Error in text generation: {e}")
            raise
