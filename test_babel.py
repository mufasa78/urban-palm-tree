from flask import Flask, render_template_string, request, session, g
from flask_babel import Babel

app = Flask(__name__)
app.secret_key = 'test_key'

# Configure available languages
LANGUAGES = ['en', 'zh']

# Initialize Babel
babel = Babel(app, default_locale='en')

@app.before_request
def before_request():
    # Set the language for the current request
    lang = request.args.get('lang')
    if lang and lang in LANGUAGES:
        session['lang'] = lang
    
    # Get language from session or default to English
    g.lang = session.get('lang', 'en')

@app.route('/')
def index():
    template = '''
    <!DOCTYPE html>
    <html lang="{{ g.lang }}">
    <head>
        <meta charset="UTF-8">
        <title>Test</title>
    </head>
    <body>
        <h1>Language Test</h1>
        <p>Current language: {{ g.lang }}</p>
        <ul>
            <li><a href="?lang=en">English</a></li>
            <li><a href="?lang=zh">Chinese</a></li>
        </ul>
    </body>
    </html>
    '''
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)
