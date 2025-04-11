# Internationalization (i18n) Support for TextWeaverAI

This document explains how the internationalization (i18n) features are implemented in the TextWeaverAI project.

## Overview

The application now supports multiple languages, with English (en) as the default language and Chinese (zh) as an additional language. The UI will automatically detect the user's preferred language from their browser settings, or they can manually switch languages using the language selector in the top-right corner of the application.

## Implementation Details

### Technologies Used

- **Flask-Babel**: For internationalization support in the Flask application
- **Jinja2 Templates**: For marking translatable strings in the HTML templates
- **JavaScript**: For handling translated text in the client-side code
- **CSS**: For ensuring proper font support for all languages

### Key Files

- **app.py**: Contains the Flask-Babel configuration and language selection logic
- **babel.cfg**: Configuration file for Flask-Babel
- **translations/**: Directory containing all translation files
  - **messages.pot**: Template file containing all translatable strings
  - **en/LC_MESSAGES/messages.po**: English translations
  - **zh/LC_MESSAGES/messages.po**: Chinese translations
  - **en/LC_MESSAGES/messages.mo**: Compiled English translations
  - **zh/LC_MESSAGES/messages.mo**: Compiled Chinese translations
- **compile_translations.py**: Script to compile .po files to .mo files
- **templates/index.html**: HTML template with translatable strings marked with `{{ _('...') }}`
- **static/js/app.js**: JavaScript file with support for language-specific text
- **static/css/styles.css**: CSS file with font support for Chinese characters

## How to Use

### Switching Languages

Users can switch languages by clicking on the language selector in the top-right corner of the application. The application will remember the selected language for the duration of the session.

### Adding New Translations

To add a new language:

1. Create a new directory under `translations/` with the language code (e.g., `translations/fr/LC_MESSAGES/` for French)
2. Copy `messages.pot` to the new directory as `messages.po`
3. Translate all strings in the `messages.po` file
4. Run `python compile_translations.py` to compile the translations
5. Update the `APP_LANGUAGES` list in `app.py` to include the new language code
6. Add the new language to the language selector in `templates/index.html`
7. Add language-specific prompts in `static/js/app.js` if needed

### Updating Translations

When you add or modify translatable strings in the application:

1. Update the `messages.pot` file with the new strings
2. Update all language-specific `messages.po` files
3. Run `python compile_translations.py` to recompile the translations

## Best Practices

- Always use the `_()` function to mark translatable strings in Python code
- Always use `{{ _('...') }}` to mark translatable strings in Jinja2 templates
- Use data attributes to pass translated strings to JavaScript
- Ensure all user-facing text is translatable
- Test the application with different languages to ensure proper display

## Font Support

The application uses a font stack that includes fonts with good support for Chinese characters:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Noto Sans CJK SC', 'Microsoft YaHei', '微软雅黑', sans-serif;
```

This ensures that Chinese text is displayed correctly on all platforms.

## Troubleshooting

If translations are not working:

1. Make sure the compiled `.mo` files exist
2. Check that the language code is included in `APP_LANGUAGES` in `app.py`
3. Verify that the browser's language settings are correctly detected
4. Clear browser cache and cookies
5. Check the Flask application logs for any errors related to Babel or translations
