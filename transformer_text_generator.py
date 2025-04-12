import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

class TransformerTextGenerator:
    def __init__(self, model_name="distilgpt2"):
        """
        Initialize the text generator with a transformer-based model.
        
        Args:
            model_name (str): The name of the model to use (default: distilgpt2)
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        
        try:
            self.logger.info(f"Loading transformer model: {model_name}")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Set seed for reproducibility
            set_seed(42)
            
            # Check if GPU is available and move model to GPU if possible
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            
            self.logger.info(f"Transformer model loaded successfully on {self.device}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize transformer model: {e}")
            raise
    
    def generate_text(self, prompt, max_length=150, temperature=0.7, num_return_sequences=1):
        """
        Generate text based on the given prompt using a transformer model.
        
        Args:
            prompt (str): The input text to base generation on
            max_length (int): Maximum length of the generated text
            temperature (float): Controls randomness (higher = more random)
            num_return_sequences (int): Number of text sequences to return
            
        Returns:
            str: The generated text
        """
        try:
            self.logger.info(f"Generating text for prompt: {prompt}")
            
            # Encode the prompt
            input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            
            # Calculate appropriate max_length based on input
            prompt_length = len(input_ids[0])
            generation_length = min(max_length, 512) - prompt_length  # Limit to model's context window
            
            # Generate text
            with torch.no_grad():
                output = self.model.generate(
                    input_ids,
                    max_length=prompt_length + generation_length,
                    temperature=temperature,
                    num_return_sequences=num_return_sequences,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    no_repeat_ngram_size=2,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the generated text
            generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            self.logger.info("Text generation successful")
            return generated_text
            
        except Exception as e:
            self.logger.error(f"Error in text generation: {e}")
            raise
    
    def get_model_info(self):
        """
        Get information about the loaded model.
        
        Returns:
            dict: Information about the model
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "parameters": sum(p.numel() for p in self.model.parameters()),
            "tokenizer_vocab_size": len(self.tokenizer)
        }
