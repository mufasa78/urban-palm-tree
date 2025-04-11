import os
import subprocess

def compile_translations():
    """Compile all translation files."""
    print("Compiling translation files...")
    
    # Get the directory of this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the translations directory
    translations_dir = os.path.join(base_dir, 'translations')
    
    # Check if the translations directory exists
    if not os.path.exists(translations_dir):
        print(f"Error: Translations directory not found at {translations_dir}")
        return False
    
    # Compile each language
    for lang in os.listdir(translations_dir):
        lang_path = os.path.join(translations_dir, lang)
        
        # Skip if not a directory or if it's the template file
        if not os.path.isdir(lang_path) or lang == 'messages.pot':
            continue
        
        # Path to the messages.po file
        po_file = os.path.join(lang_path, 'LC_MESSAGES', 'messages.po')
        
        if not os.path.exists(po_file):
            print(f"Warning: No messages.po file found for language {lang}")
            continue
        
        # Compile the .po file to .mo
        try:
            mo_dir = os.path.dirname(po_file)
            mo_file = os.path.join(mo_dir, 'messages.mo')
            
            # Use pybabel or msgfmt to compile
            try:
                # Try using pybabel first
                subprocess.run(['pybabel', 'compile', '-f', '-i', po_file, '-o', mo_file], check=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                try:
                    # Fall back to msgfmt
                    subprocess.run(['msgfmt', po_file, '-o', mo_file], check=True)
                except (subprocess.SubprocessError, FileNotFoundError):
                    # Manual compilation if tools are not available
                    print(f"Warning: Could not compile {po_file} using pybabel or msgfmt")
                    print(f"Please install babel or gettext tools to compile translations")
                    return False
            
            print(f"Successfully compiled translations for {lang}")
        except Exception as e:
            print(f"Error compiling translations for {lang}: {e}")
            return False
    
    print("All translations compiled successfully!")
    return True

if __name__ == "__main__":
    compile_translations()
