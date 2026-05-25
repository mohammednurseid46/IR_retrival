import os

class StopwordRemover:
    def __init__(self, english_path=None, amharic_path=None):
        # Default paths relative to project root (assuming src/preprocessing/stopword_remover.py)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        if not english_path:
            english_path = os.path.join(base_dir, 'data', 'stopwords', 'english_stopwords.txt')
        if not amharic_path:
            amharic_path = os.path.join(base_dir, 'data', 'stopwords', 'amharic_stopwords.txt')

        self.english_stopwords = self._load_stopwords(english_path)
        self.amharic_stopwords = self._load_stopwords(amharic_path)

    def _load_stopwords(self, file_path):
        stopwords = set()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip()
                        if word:
                            stopwords.add(word.lower())
            except Exception as e:
                print(f"Warning: Could not load stopwords from {file_path}: {e}")
        else:
            print(f"Warning: Stopword file not found at {file_path}")
        return stopwords

    def remove_stopwords(self, tokens, language='english'):
        """Remove stopwords from a list of tokens based on the language."""
        if language.lower() == 'amharic':
            stopwords = self.amharic_stopwords
        else:
            stopwords = self.english_stopwords
            
        return [token for token in tokens if token.lower() not in stopwords]
