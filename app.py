import os
import logging
from flask import Flask, render_template, request, jsonify, session, g
from flask_babel import Babel, gettext as _

# Import text generator
from text_generator import TextGenerator

# Comment out transformer import until dependencies are installed
# from transformer_text_generator import TransformerTextGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

# Configure available languages
APP_LANGUAGES = ['en', 'zh']

# Function to select locale for Flask-Babel
def get_locale():
    # Get language from session or request parameter
    lang = request.args.get('lang')
    if lang and lang in APP_LANGUAGES:
        session['lang'] = lang
    return session.get('lang', 'en')

# Initialize Babel for internationalization
babel = Babel(app, default_locale='en', default_timezone='UTC', locale_selector=get_locale)

@app.before_request
def before_request():
    # Set the language for the current request
    lang = request.args.get('lang')
    if lang and lang in APP_LANGUAGES:
        session['lang'] = lang

    # Get language from session or default to English
    g.lang = session.get('lang', 'en')

# Initialize the text generator model
text_generator = None

# Flag to determine which generator to use (set to False to use Markov only)
USE_TRANSFORMER = False

try:
    # Load Markov chain model
    logger.info("Loading Markov chain text generation model...")
    text_generator = TextGenerator()
    logger.info("Markov chain model loaded successfully!")

    # Transformer model code is commented out until dependencies are installed
    # logger.info("Loading transformer text generation model...")
    # transformer_generator = TransformerTextGenerator(model_name="distilgpt2")
    # logger.info(f"Transformer model loaded successfully on {transformer_generator.device}!")
    # model_info = transformer_generator.get_model_info()
    # logger.info(f"Model: {model_info['model_name']}, Parameters: {model_info['parameters']:,}, Device: {model_info['device']}")

except Exception as e:
    logger.error(f"Error loading text generation model: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    # Check if model is available
    if text_generator is None:
        return jsonify({'error': 'Text generation model not loaded. Please check the logs.'}), 500

    try:
        data = request.json
        prompt = data.get('prompt', '')
        model_type = data.get('model_type', 'markov')  # Always use markov for now

        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        # Generate text using Markov model
        generated_text = text_generator.generate_text(prompt)
        model_used = 'markov'

        return jsonify({
            'generated_text': generated_text,
            'model_used': model_used
        })

    except Exception as e:
        logger.error(f"Error during text generation: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
