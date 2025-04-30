import os
import logging
import pandas as pd
from flask import Flask, render_template, request, jsonify, session, g
from flask_babel import Babel, gettext as _
from deep_translator import GoogleTranslator

# Import text generators
from text_generator import TextGenerator
from transformer_text_generator import TransformerTextGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

# Configure available language (Chinese only)
APP_LANGUAGES = ['zh']

# Available topics and their translations
TOPICS = {
    'Animals': '动物',
    'Books': '书籍',
    'Climate': '气候',
    'Environment': '环境',
    'Friends': '朋友',
    'Hospital': '医院',
    'Movies': '电影',
    'Religion': '宗教',
    'School': '学校',
    'Space': '太空'
}

# Function to select locale for Flask-Babel
def get_locale():
    return 'zh'  # Always return Chinese

# Initialize Babel for internationalization
babel = Babel(app, default_locale='zh', default_timezone='UTC', locale_selector=get_locale)

@app.before_request
def before_request():
    # Set language to Chinese
    g.lang = 'zh'
    
    # Make topics available to templates
    g.topics = TOPICS

def load_datasets():
    """Load all available datasets"""
    datasets = {}
    try:
        for topic_en in TOPICS.keys():
            file_path = f"dataset/{topic_en}.csv"
            try:
                df = pd.read_csv(file_path)
                datasets[topic_en] = df
                logger.info(f"Loaded dataset: {topic_en}")
            except Exception as e:
                logger.error(f"Error loading dataset {file_path}: {e}")
    except Exception as e:
        logger.error(f"Error loading datasets: {e}")
    return datasets

# Initialize text generators
generators = {
    'markov': TextGenerator(),
    'transformer': TransformerTextGenerator(model_name="distilgpt2")
}

# Load datasets
datasets = load_datasets()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        model_type = data.get('model_type', 'transformer')
        selected_topic = data.get('topic', None)

        if not prompt:
            return jsonify({'error': _('请输入关键词或短语')}), 400

        # Get the appropriate generator
        text_generator = generators.get(model_type)
        if not text_generator:
            return jsonify({'error': _('无效的模型类型')}), 400

        # Get topic-specific data if a topic is selected
        topic_data = None
        if selected_topic and selected_topic in datasets:
            topic_data = datasets[selected_topic]

        # Generate text
        generated_text = text_generator.generate_text(
            prompt=prompt,
            max_length=300,
            topic_data=topic_data
        )

        # Ensure text is in Chinese
        if g.lang == 'zh':
            try:
                logger.info(f"Translating text to Chinese: {generated_text[:50]}...")
                translator = GoogleTranslator(source='en', target='zh-CN')
                generated_text = translator.translate(generated_text)
                logger.info(f"Translation successful: {generated_text[:50]}...")
            except Exception as e:
                logger.error(f"Translation error: {e}")

        return jsonify({
            'generated_text': generated_text,
            'model_used': model_type
        })

    except Exception as e:
        logger.error(f"Error during text generation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/change_model', methods=['POST'])
def change_model():
    try:
        data = request.get_json()
        model_type = data.get('model_type')
        if model_type not in ['transformer', 'markov']:
            return jsonify({'error': _('无效的模型类型')}), 400
        session['model_type'] = model_type
        return jsonify({'success': True, 'model_type': model_type})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
