import logging
import random
import re
from collections import defaultdict
import pandas as pd
import os
from deep_translator import GoogleTranslator

class TextGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.corpus = {}
        self.markov_chain = defaultdict(list)
        self.datasets = {}
        self.translator = GoogleTranslator(source='en', target='zh-CN')

        try:
            self.logger.info("Initializing text generator with datasets")
            self._load_datasets()
            self._initialize_corpus()
            self._build_markov_model()
            self.logger.info("Text generator initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize text generator: {e}")
            raise

    def _load_datasets(self):
        """Load all available CSV datasets"""
        dataset_path = "dataset"
        for file in os.listdir(dataset_path):
            if file.endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(dataset_path, file))
                    category = file.replace('.csv', '')
                    self.datasets[category] = df
                    self.logger.info(f"Loaded dataset: {category}")
                except Exception as e:
                    self.logger.error(f"Error loading dataset {file}: {e}")

    def _initialize_corpus(self):
        """Initialize the corpus with data from CSV files and predefined samples"""
        # Load data from datasets into corpus
        for category, df in self.datasets.items():
            self.corpus[category] = []
            for _, row in df.iterrows():
                # Assuming the CSV has a 'text' or similar column
                # Adjust the column name based on your CSV structure
                for col in df.columns:
                    if isinstance(row[col], str) and len(row[col]) > 10:
                        self.corpus[category].append(row[col])

    def _build_markov_model(self):
        """Build a Markov chain model from the corpus"""
        for category, texts in self.corpus.items():
            for text in texts:
                if not isinstance(text, str):
                    continue
                words = text.split()
                for i in range(len(words) - 1):
                    self.markov_chain[words[i]].append(words[i + 1])
                # Add sentence endings
                if len(words) > 0:
                    self.markov_chain[words[-1]].append(None)

    def _get_matching_category(self, prompt, topic_data=None):
        """Find the most relevant category for the given prompt"""
        if topic_data is not None:
            return topic_data.name if hasattr(topic_data, 'name') else 'general'

        prompt_lower = prompt.lower()
        # Check for keyword matches in categories
        for category in self.corpus.keys():
            if category.lower() in prompt_lower:
                return category

        # Default to a random category if no match
        return random.choice(list(self.corpus.keys()))

    def generate_text(self, prompt, max_length=150, temperature=0.7, topic_data=None):
        """Generate text based on the given prompt"""
        try:
            self.logger.info(f"Generating text for prompt: {prompt}")

            # Translate prompt to English for processing if it's in Chinese
            try:
                en_prompt = GoogleTranslator(source='zh-CN', target='en').translate(prompt)
            except:
                en_prompt = prompt

            # Clean and prepare the prompt
            words = re.findall(r'\w+', en_prompt.lower())
            if not words:
                words = ["the"]

            # Determine relevant category and get starter text
            category = self._get_matching_category(en_prompt, topic_data)
            
            # Use topic-specific data if available
            if topic_data is not None:
                relevant_texts = []
                for col in topic_data.columns:
                    texts = topic_data[col].dropna().astype(str).tolist()
                    relevant_texts.extend([t for t in texts if len(t) > 10])
                if relevant_texts:
                    starter_text = random.choice(relevant_texts)
                else:
                    starter_text = random.choice(self.corpus[category])
            else:
                starter_text = random.choice(self.corpus[category])

            # Generate text using the Markov chain
            result = []
            current_word = words[-1] if words else starter_text.split()[0]
            word_count = 0

            while word_count < max_length:
                if current_word not in self.markov_chain or not self.markov_chain[current_word]:
                    next_words = []
                    if topic_data is not None:
                        for col in topic_data.columns:
                            texts = topic_data[col].dropna().astype(str).tolist()
                            for text in texts:
                                next_words.extend(text.split())
                    if not next_words:
                        next_words = starter_text.split()
                    next_word = random.choice(next_words)
                else:
                    next_word = random.choice(self.markov_chain[current_word])

                if next_word is None:
                    break

                result.append(next_word)
                current_word = next_word
                word_count += 1

            generated_part = ' '.join(result)
            generated_part = re.sub(r'\s+([.,;:!?)])', r'\1', generated_part)
            generated_part = re.sub(r'(\()\s+', r'\1', generated_part)

            # Combine with the original prompt
            generated_text = f"{prompt} {generated_part}"

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
