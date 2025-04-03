import os
import logging
from flask import Flask, render_template, request, jsonify

from text_generator import TextGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

# Initialize the text generator model
text_generator = None

try:
    logger.info("Loading text generation model...")
    text_generator = TextGenerator()
    logger.info("Text generation model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading text generation model: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    if text_generator is None:
        return jsonify({'error': 'Text generation model not loaded. Please check the logs.'}), 500
    
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Generate text based on the prompt
        generated_text = text_generator.generate_text(prompt)
        
        return jsonify({
            'generated_text': generated_text
        })
        
    except Exception as e:
        logger.error(f"Error during text generation: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
