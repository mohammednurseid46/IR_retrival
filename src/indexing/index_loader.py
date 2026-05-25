import os
from .inverted_index import InvertedIndex

class IndexLoader:
    @staticmethod
    def load_index(language, processed_dir=None):
        """Loads and returns an InvertedIndex for the specified language."""
        if not processed_dir:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            processed_dir = os.path.join(base_dir, 'data', 'processed')
            
        index_file = os.path.join(processed_dir, f"{language.lower()}_index.json")
        
        index = InvertedIndex()
        if os.path.exists(index_file):
            index.load(index_file)
            return index
        else:
            raise FileNotFoundError(f"Inverted index for {language} not found at {index_file}. Run index builder first.")
            
    @staticmethod
    def load_both_indexes(processed_dir=None):
        """Loads both English and Amharic indexes, returning a dictionary."""
        return {
            'english': IndexLoader.load_index('english', processed_dir),
            'amharic': IndexLoader.load_index('amharic', processed_dir)
        }
