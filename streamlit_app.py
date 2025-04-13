import streamlit as st
import logging
import random
import re
import torch
from collections import defaultdict
from deep_translator import GoogleTranslator

# Import the transformer text generator
from transformer_text_generator import TransformerTextGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration first - this must be the first Streamlit command
st.set_page_config(
    page_title="AI Text Generator",
    page_icon="📝",
    layout="wide"
)

# Define translations
translations = {
    'en': {
        'app_title': 'AI Text Generator',
        'language': 'Language',
        'app_description': 'Enter a keyword or phrase and let AI generate text for you',
        'educational_note': 'This is an educational tool that demonstrates how machine learning models can generate text based on input prompts.',
        'input_label': 'Enter a keyword or short sentence:',
        'input_placeholder': 'Example: "The future of technology"',
        'generate_button': 'Generate Text',
        'output_title': 'Generated Text',
        'output_placeholder': 'Generated text will appear here...',
        'how_it_works': 'How It Works',
        'step1_title': '1. Input Processing',
        'step1_desc': 'Your input is tokenized (split into pieces that the model can understand) and preprocessed.',
        'step2_title': '2. Model Generation',
        'step2_desc': 'A Markov chain text model finds patterns and generates coherent text based on your input.',
        'step3_title': '3. Text Output',
        'step3_desc': 'The model\'s output is decoded back into human-readable text and displayed to you.',
        'footer': 'Educational Text Generation Project | Using Streamlit & Markov Chain Models',
        'error_empty_prompt': 'Please enter a keyword or phrase.',
        'error_generation': 'An error occurred while generating text.',
        'example_prompts': [
            "The future of technology",
            "Once upon a time",
            "Climate change is",
            "Artificial intelligence will",
            "The most important invention"
        ]
    },
    'zh': {
        'app_title': 'AI文本生成器',
        'language': '语言',
        'app_description': '输入关键词或短语，让AI为您生成文本',
        'educational_note': '这是一个教育工具，展示机器学习模型如何基于输入提示生成文本。',
        'input_label': '输入关键词或短句：',
        'input_placeholder': '示例："科技的未来"',
        'generate_button': '生成文本',
        'output_title': '生成的文本',
        'output_placeholder': '生成的文本将显示在这里...',
        'how_it_works': '工作原理',
        'step1_title': '1. 输入处理',
        'step1_desc': '您的输入被标记化（分割成模型可以理解的片段）并预处理。',
        'step2_title': '2. 模型生成',
        'step2_desc': '马尔可夫链文本模型找到模式并基于您的输入生成连贯的文本。',
        'step3_title': '3. 文本输出',
        'step3_desc': '模型的输出被解码回人类可读的文本并显示给您。',
        'footer': '教育文本生成项目 | 使用Streamlit和马尔可夫链模型',
        'error_empty_prompt': '请输入关键词或短语。',
        'error_generation': '生成文本时发生错误。',
        'example_prompts': [
            "科技的未来",
            "从前有一个",
            "气候变化是",
            "人工智能将会",
            "最重要的发明"
        ]
    }
}

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

            # Don't just repeat the prompt - start with it but then generate new content
            result = []  # We'll add the prompt back at the end
            word_count = 0

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

                # Add some variety by occasionally inserting phrases from the corpus
                if word_count % 20 == 0 and random.random() < 0.3:
                    random_text = random.choice(self.corpus[category]).split()
                    insert_phrase = random_text[1:min(5, len(random_text))]
                    result.extend(insert_phrase)
                    current_word = insert_phrase[-1] if insert_phrase else current_word
                    word_count += len(insert_phrase)

                # Add some randomness for sentence endings
                if next_word.endswith(('.', '!', '?')) and random.random() < 0.3:
                    break

            # Combine the prompt with the generated text
            if len(result) > 0:
                # Join all words into a coherent text
                generated_part = ' '.join(result)

                # Clean up spacing around punctuation
                generated_part = re.sub(r'\s+([.,;:!?)])', r'\1', generated_part)
                generated_part = re.sub(r'(\()\s+', r'\1', generated_part)

                # Make sure we have enough text (at least 100 characters)
                if len(generated_part) < 100:
                    # Add more text from the corpus
                    additional_text = random.choice(self.corpus[category])
                    generated_part += " " + additional_text

                # Combine with the prompt
                generated_text = f"{prompt} {generated_part}"
            else:
                # Fallback if no text was generated
                sample_texts = [random.choice(self.corpus[category]) for _ in range(3)]
                generated_text = f"{prompt} {' '.join(sample_texts)}"

            self.logger.info("Text generation successful")
            return generated_text

        except Exception as e:
            self.logger.error(f"Error in text generation: {e}")
            raise

# Initialize the text generators and translator
@st.cache_resource
def load_text_generators():
    generators = {
        'markov': TextGenerator(),
        'transformer': TransformerTextGenerator(model_name="distilgpt2")
    }
    return generators

# No need to initialize translator as we'll create it when needed

def main():
    # Initialize session state for language and model type if they don't exist
    if 'language' not in st.session_state:
        st.session_state.language = 'en'

    if 'model_type' not in st.session_state:
        st.session_state.model_type = 'transformer'

    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = None

    # Load text generators
    generators = load_text_generators()

    # Get translations for the current language
    t = translations[st.session_state.language]

    # Add custom CSS for Chinese font support
    st.markdown("""
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Noto Sans CJK SC', 'Microsoft YaHei', '微软雅黑', sans-serif;
    }
    .stButton button {
        width: 100%;
    }
    .output-area {
        min-height: 150px;
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar for language and model selection
    with st.sidebar:
        st.title(t['language'])
        if st.button("English", key="en_button", disabled=st.session_state.language == 'en'):
            st.session_state.language = 'en'
            st.rerun()
        if st.button("中文 (Chinese)", key="zh_button", disabled=st.session_state.language == 'zh'):
            st.session_state.language = 'zh'
            st.rerun()

        # Model selector
        st.title("Model")
        if st.button("Transformer (DistilGPT-2)", key="transformer_button", disabled=st.session_state.model_type == 'transformer'):
            st.session_state.model_type = 'transformer'
            st.rerun()
        if st.button("Markov Chain", key="markov_button", disabled=st.session_state.model_type == 'markov'):
            st.session_state.model_type = 'markov'
            st.rerun()

        # Show model info
        if st.session_state.model_type == 'transformer':
            st.info("DistilGPT-2: A smaller, faster version of GPT-2 with 82M parameters.")
        else:
            st.info("Markov Chain: A simple statistical model that predicts the next word based on previous words.")

    # Main content
    st.title(t['app_title'])
    st.markdown(t['app_description'])

    # Information box
    st.info(t['educational_note'])

    # Load the text generators
    generators = load_text_generators()
    text_generator = generators[st.session_state.model_type]

    # Input section
    st.subheader(t['input_label'])

    # Get a random example prompt for the placeholder
    random_placeholder = random.choice(t['example_prompts'])

    # Create two columns for input and button
    col1, col2 = st.columns([3, 1])
    with col1:
        prompt = st.text_input(
            label="",
            placeholder=random_placeholder,
            key="prompt_input"
        )
    with col2:
        generate_button = st.button(t['generate_button'], key="generate_button")

    # Output section
    st.subheader(t['output_title'])

    # Create a placeholder for the output
    output_placeholder = st.empty()

    # Initialize with placeholder text
    if 'generated_text' not in st.session_state:
        output_placeholder.markdown(f"*{t['output_placeholder']}*")
    else:
        output_placeholder.markdown(st.session_state.generated_text)

    # Generate text when button is clicked
    if generate_button:
        if not prompt:
            st.error(t['error_empty_prompt'])
        else:
            try:
                with st.spinner():
                    # Get the selected model
                    model_type = st.session_state.model_type
                    text_generator = generators[model_type]

                    # Use the selected model
                    generated_text = text_generator.generate_text(prompt, max_length=200)  # Increase max_length for more text

                    # Translate text if language is Chinese
                    if st.session_state.language == "zh":
                        try:
                            logger.info(f"Translating text to Chinese: {generated_text[:50]}...")
                            translator = GoogleTranslator(source='en', target='zh-CN')
                            generated_text = translator.translate(generated_text)
                            logger.info(f"Translation successful: {generated_text[:50]}...")
                        except Exception as e:
                            logger.error(f"Translation error: {e}")
                            # Continue with untranslated text if translation fails

                    st.session_state.generated_text = generated_text

                    # Display model used and generated text
                    output_placeholder.markdown(f"**Model used:** {st.session_state.model_type.capitalize()}")

                    # Format the output to clearly show the generated text
                    if generated_text.startswith(prompt):
                        # Highlight the prompt part differently
                        prompt_part = prompt
                        generated_part = generated_text[len(prompt):]

                        # Make sure we have meaningful generated text
                        if len(generated_part.strip()) < 10:
                            # If generated part is too short, regenerate with different model
                            logger.warning("Generated text too short, trying with different parameters")
                            if st.session_state.model_type == 'transformer':
                                # Try with Markov model instead
                                backup_generator = generators['markov']
                                generated_text = backup_generator.generate_text(prompt, max_length=300)
                            else:
                                # Try with transformer model instead
                                backup_generator = generators['transformer']
                                generated_text = backup_generator.generate_text(prompt, max_length=300)

                            # Check if the new text starts with the prompt
                            if generated_text.startswith(prompt):
                                prompt_part = prompt
                                generated_part = generated_text[len(prompt):]
                            else:
                                prompt_part = ""
                                generated_part = generated_text

                        formatted_text = f"""
                        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                            <span style='color: #555; font-style: italic;'>{prompt_part}</span>
                            <span style='color: #000;'>{generated_part}</span>
                        </div>
                        """
                    else:
                        formatted_text = f"""
                        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                            <span style='color: #000;'>{generated_text}</span>
                        </div>
                        """

                    output_placeholder.markdown(formatted_text, unsafe_allow_html=True)

                    # Also display the raw text in a code block for clarity
                    with st.expander("Show raw generated text"):
                        st.code(generated_text)
            except Exception as e:
                st.error(f"{t['error_generation']} {str(e)}")

    # How it works section
    st.markdown("---")
    st.subheader(t['how_it_works'])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**{t['step1_title']}**")
        st.markdown(t['step1_desc'])

    with col2:
        st.markdown(f"**{t['step2_title']}**")
        st.markdown(t['step2_desc'])

    with col3:
        st.markdown(f"**{t['step3_title']}**")
        st.markdown(t['step3_desc'])

    # Footer
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: gray;'>{t['footer']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
