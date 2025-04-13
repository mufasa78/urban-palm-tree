import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class TransformerTextGenerator:
    def __init__(self, model_name="distilgpt2"):
        """
        Initialize the transformer text generator with a pre-trained model.

        Args:
            model_name (str): The name of the pre-trained model to use
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name

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

    def generate_text(self, prompt, max_length=150, temperature=0.7, num_return_sequences=1):
        """
        Generate text based on the given prompt using the transformer model.

        Args:
            prompt (str): The input text to base generation on
            max_length (int): Maximum length of the generated text
            temperature (float): Controls randomness (higher = more random)
            num_return_sequences (int): Number of text sequences to generate

        Returns:
            str: The generated text
        """
        try:
            self.logger.info(f"Generating text for prompt: {prompt}")

            # Simple encoding without padding to avoid issues
            input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

            # Calculate appropriate max_length for the model
            input_length = len(input_ids[0])
            # Ensure we generate a substantial amount of text (at least 100 tokens)
            generation_length = max(100, min(max_length, 1024 - input_length))  # Most models have a context limit of 1024

            self.logger.info(f"Input length: {input_length}, Generation length: {generation_length}")

            # Generate text using a more creative approach
            with torch.no_grad():
                self.logger.info("Starting text generation with transformer model...")
                output = self.model.generate(
                    input_ids,
                    max_length=input_length + generation_length,
                    do_sample=True,  # Enable sampling
                    top_k=50,         # Consider top 50 tokens
                    top_p=0.95,       # Increase nucleus sampling probability
                    temperature=0.8,   # Slightly higher temperature for more creativity
                    repetition_penalty=1.2,  # Penalize repetition
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3  # Avoid repeating 3-grams
                )
                self.logger.info(f"Generation complete. Output shape: {output.shape}")

            # Decode the generated text
            generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

            # Check if we're just returning the prompt
            if generated_text.strip() == prompt.strip() or len(generated_text) < len(prompt) + 10:
                self.logger.warning("Generated text is too similar to the prompt. Trying again with different parameters.")
                # Try a completely different approach for generation
                try:
                    # Use the model directly for text generation
                    encoded_input = self.tokenizer(prompt, return_tensors='pt').to(self.device)
                    outputs = self.model(**encoded_input)
                    next_token_logits = outputs.logits[:, -1, :]

                    # Get the most likely next tokens
                    probs = torch.softmax(next_token_logits, dim=-1)
                    top_k_probs, top_k_indices = torch.topk(probs, k=5, dim=-1)

                    # Choose one of the top tokens
                    chosen_idx = top_k_indices[0, torch.multinomial(top_k_probs[0], num_samples=1)]
                    generated_ids = torch.cat([encoded_input.input_ids, chosen_idx.unsqueeze(0).unsqueeze(0)], dim=-1)

                    # Continue generating tokens
                    for _ in range(generation_length):
                        outputs = self.model(input_ids=generated_ids)
                        next_token_logits = outputs.logits[:, -1, :]
                        probs = torch.softmax(next_token_logits, dim=-1)
                        top_k_probs, top_k_indices = torch.topk(probs, k=5, dim=-1)
                        chosen_idx = top_k_indices[0, torch.multinomial(top_k_probs[0], num_samples=1)]
                        generated_ids = torch.cat([generated_ids, chosen_idx.unsqueeze(0).unsqueeze(0)], dim=-1)

                        # Stop if we generate an EOS token
                        if chosen_idx.item() == self.tokenizer.eos_token_id:
                            break

                    # Decode the generated text
                    generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
                except Exception as e:
                    self.logger.warning(f"Alternative generation method failed: {e}")
                    # Fall back to a simpler approach
                    output = self.model.generate(
                        input_ids,
                        max_length=input_length + generation_length,
                        num_beams=5,
                        no_repeat_ngram_size=2,
                        num_return_sequences=1,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                    generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

            self.logger.info(f"Text generation successful. Generated {len(generated_text)} characters.")
            return generated_text

        except Exception as e:
            self.logger.error(f"Error in text generation: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            # Fallback to a simpler method if the advanced one fails
            try:
                self.logger.info("Attempting fallback generation method...")
                input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
                output = self.model.generate(
                    input_ids,
                    max_length=input_length + 50,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
                return generated_text
            except Exception as e2:
                self.logger.error(f"Fallback generation also failed: {e2}")
                # Return a message if all else fails
                return f"{prompt} [Error: Unable to generate text with the transformer model. Please try again with a different prompt or model.]"
