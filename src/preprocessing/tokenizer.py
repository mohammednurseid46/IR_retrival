import re

class Tokenizer:
    def __init__(self):
        # Ethiopic word space (፡), full stop (።), comma (፣), semicolon (፤), preface colon (፦)
        self.amharic_punctuation_pattern = re.compile(r'[፡።፣፤፦፥፧፨\?\!\.\,\;\:\"\-\(\)]')
        # Standard English punctuation
        self.english_punctuation_pattern = re.compile(r'[^a-zA-Z0-9\s]')

    def tokenize_english(self, text):
        """Tokenize English text into lowercase words, removing punctuation."""
        if not text:
            return []
        text = text.lower()
        # Replace punctuation with space to avoid merging words
        cleaned = self.english_punctuation_pattern.sub(' ', text)
        return [word for word in cleaned.split() if word.strip()]

    def tokenize_amharic(self, text):
        """Tokenize Amharic text, handling Ethiopic separators and punctuation."""
        if not text:
            return []
        # Replace Ethiopic punctuation and separators with space
        cleaned = self.amharic_punctuation_pattern.sub(' ', text)
        # Split by whitespace
        return [word for word in cleaned.split() if word.strip()]

    def tokenize(self, text, language='english'):
        """Main tokenize method routing to language-specific tokenizers."""
        if language.lower() == 'amharic':
            return self.tokenize_amharic(text)
        return self.tokenize_english(text)
