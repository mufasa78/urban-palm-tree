import os
import logging
import random
import re
from collections import defaultdict

class TextGenerator:
    def __init__(self, model_name=None):
        """
        Initialize the text generator with a simple Markov chain approach.
        This is a lightweight educational implementation that doesn't require ML libraries.
        
        Args:
            model_name (str): Not used in this implementation, kept for API compatibility
        """
        self.logger = logging.getLogger(__name__)
        self.corpus = {}
        self.markov_chain = defaultdict(list)
        
        try:
            self.logger.info("Initializing educational text generator")
            
            # Load or create corpus with predefined text samples
            self._initialize_corpus()
            
            # Build Markov chain model from the corpus
            self._build_markov_model()
            
            self.logger.info("Text generator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize text generator: {e}")
            raise
    
    def _initialize_corpus(self):
        """Initialize the corpus with predefined text samples"""
        self.corpus = {
            "technology": [
                "Technology continues to evolve at an unprecedented pace, transforming how we live, work, and interact.",
                "Artificial intelligence and machine learning are revolutionizing industries across the globe.",
                "The future of technology lies in sustainable innovation that addresses global challenges.",
                "Emerging technologies like quantum computing promise to solve problems previously thought impossible.",
                "Smart devices and the Internet of Things are creating interconnected ecosystems of technology."
            ],
            "science": [
                "Scientific discoveries expand our understanding of the natural world and our place in it.",
                "Research in genetics and biotechnology is opening new frontiers in medicine and healthcare.",
                "Climate science provides crucial insights for addressing environmental challenges.",
                "Astronomy and space exploration reveal the mysteries of our universe and beyond.",
                "Collaborative scientific efforts across disciplines lead to breakthrough innovations."
            ],
            "education": [
                "Education empowers individuals to reach their full potential and contribute to society.",
                "Modern learning approaches combine traditional methods with digital innovations.",
                "Accessible education is essential for creating equitable opportunities for all.",
                "Critical thinking and problem-solving skills are fundamental to educational success.",
                "Lifelong learning has become necessary in our rapidly changing world."
            ],
            "storytelling": [
                "Once upon a time in a land far away, there lived a wise old wizard with magical powers.",
                "The young explorer ventured into the dense forest, unaware of the adventures that awaited.",
                "As the sun set over the ancient city, shadows revealed secrets hidden for centuries.",
                "The mysterious message appeared exactly at midnight, changing everything forever.",
                "Against all odds, the unlikely heroes joined forces to overcome the greatest challenge."
            ]
        }
    
    def _build_markov_model(self):
        """Build a simple Markov chain model from the corpus"""
        for category, texts in self.corpus.items():
            for text in texts:
                words = text.split()
                for i in range(len(words) - 1):
                    self.markov_chain[words[i]].append(words[i + 1])
                # Add sentence endings
                self.markov_chain[words[-1]].append(None)
    
    def _get_matching_category(self, prompt):
        """Find the most relevant category for the given prompt"""
        prompt_lower = prompt.lower()
        
        # Check for keyword matches in categories
        for category in self.corpus.keys():
            if category in prompt_lower:
                return category
        
        # Check for keyword matches in text samples
        for category, texts in self.corpus.items():
            for text in texts:
                if any(word in prompt_lower for word in text.lower().split()):
                    return category
        
        # Default to a random category if no match
        return random.choice(list(self.corpus.keys()))
    
    def generate_text(self, prompt, max_length=150, temperature=0.7, num_return_sequences=1):
        """
        Generate text based on the given prompt using a Markov chain approach.
        
        Args:
            prompt (str): The input text to base generation on
            max_length (int): Maximum length of the generated text
            temperature (float): Controls randomness (not fully implemented in this simple version)
            num_return_sequences (int): Number of text sequences (only returns 1 in this version)
            
        Returns:
            str: The generated text
        """
        try:
            self.logger.info(f"Generating text for prompt: {prompt}")
            
            # Clean and prepare the prompt
            prompt = prompt.strip()
            words = re.findall(r'\w+', prompt.lower())
            
            if not words:
                words = ["the"]  # Default starter if prompt is empty
            
            # Determine relevant category and get some starter text
            category = self._get_matching_category(prompt)
            starter_text = random.choice(self.corpus[category])
            starter_words = starter_text.split()[:3]  # Use first few words from a matching category
            
            # Start with the last word from the prompt or a relevant word
            if len(words) > 0:
                current_word = words[-1]
                if current_word not in self.markov_chain:
                    current_word = starter_words[0]
            else:
                current_word = starter_words[0]
            
            result = [prompt]  # Start with the original prompt
            word_count = len(prompt.split())
            
            # Generate text using the Markov chain
            while word_count < max_length:
                # If the current word isn't in our model, pick a random word from the corpus
                if current_word not in self.markov_chain or not self.markov_chain[current_word]:
                    next_words = []
                    for text in self.corpus[category]:
                        next_words.extend(text.split())
                    next_word = random.choice(next_words)
                else:
                    # Get next word based on Markov chain probabilities
                    next_word = random.choice(self.markov_chain[current_word])
                
                # Stop if we reached an end token
                if next_word is None:
                    break
                
                # Add the next word to the result
                result.append(next_word)
                current_word = next_word
                word_count += 1
                
                # Add some randomness for sentence endings
                if next_word.endswith(('.', '!', '?')) and random.random() < 0.3:
                    break
            
            # Join all words into a coherent text
            generated_text = ' '.join(result)
            
            # Clean up spacing around punctuation
            generated_text = re.sub(r'\s+([.,;:!?)])', r'\1', generated_text)
            generated_text = re.sub(r'(\()\s+', r'\1', generated_text)
            
            self.logger.info("Text generation successful")
            return generated_text
            
        except Exception as e:
            self.logger.error(f"Error in text generation: {e}")
            raise
