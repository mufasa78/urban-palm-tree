import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ChineseLLMGenerator:
    def __init__(self, model_name="THUDM/chatglm3-6b"):
        """
        Initialize the Chinese LLM text generator with a pre-trained model.
        
        Args:
            model_name (str): The name of the pre-trained model to use
                Options include:
                - "THUDM/chatglm3-6b" (ChatGLM3, good for Chinese text)
                - "Qwen/Qwen-7B" (Qwen by Alibaba, excellent for Chinese)
                - "baichuan-inc/Baichuan2-7B-Chat" (Baichuan, optimized for Chinese)
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        
        try:
            self.logger.info(f"Initializing Chinese LLM generator with model: {model_name}")
            
            # Set device (use CUDA if available, otherwise CPU)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.logger.info(f"Using device: {self.device}")
            
            # Load tokenizer and model with lower precision for efficiency
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            
            # Load model with 4-bit quantization for efficiency if on CPU
            if self.device == "cpu":
                self.logger.info("Loading model with 4-bit quantization for CPU efficiency")
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    load_in_4bit=True,
                    low_cpu_mem_usage=True
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    device_map="auto"
                )
            
            self.logger.info("Chinese LLM generator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Chinese LLM generator: {e}")
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
        Generate text based on the given prompt using the Chinese LLM model.
        
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
            
            # For ChatGLM models, use their specific generation method
            if "chatglm" in self.model_name.lower():
                response, _ = self.model.chat(self.tokenizer, prompt, history=[])
                return response
            
            # For other models, use the standard generation approach
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate with appropriate parameters for Chinese text
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    do_sample=True,
                    temperature=temperature,
                    top_p=0.9,
                    repetition_penalty=1.2,
                    num_return_sequences=num_return_sequences
                )
            
            # Decode the generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from the beginning if it's there
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
                
            # If we got empty text, try again with different parameters
            if not generated_text:
                self.logger.warning("Empty generation result, trying with different parameters")
                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_length=max_length,
                        do_sample=True,
                        temperature=1.0,  # Higher temperature for more randomness
                        top_p=0.95,
                        num_return_sequences=1
                    )
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()
            
            return generated_text
            
        except Exception as e:
            self.logger.error(f"Error in text generation: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return f"Error generating text: {str(e)}"
