import re
from langdetect import detect

class EmailPreprocessor:
    def __init__(self):
        self.spam_keywords = ['gambling', 'casino', 'free prize'] # Cite: 278

    def clean_text(self, text):
        # Remove signatures, disclaimers, and boilerplate
        text = re.sub(r'--\n.*', '', text, flags=re.DOTALL) 
        return text.strip()

    def get_signals(self, email_json):
        # Extract metadata signals
        content = email_json.get('body', '')
        return {
            "has_attachments": len(email_json.get('attachments', [])) > 0,
            "language": detect(content) if content else "unknown", # Cite: 273
            "is_spam": any(k in content.lower() for k in self.spam_keywords)
        }