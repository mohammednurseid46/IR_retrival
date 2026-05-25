import os
import json

class TranslationCache:
    def __init__(self, cache_file=None):
        if not cache_file:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            cache_file = os.path.join(base_dir, 'data', 'processed', 'translation_cache.json')
            
        self.cache_file = cache_file
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load translation cache: {e}")
        return {}

    def save_cache(self):
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Could not save translation cache: {e}")

    def get(self, text, source_lang, target_lang):
        """Retrieve translation from cache. Returns None if not cached."""
        key = f"{source_lang}->{target_lang}:{text.strip().lower()}"
        return self.cache.get(key)

    def set(self, text, translation, source_lang, target_lang):
        """Store translation in cache and persist it."""
        key = f"{source_lang}->{target_lang}:{text.strip().lower()}"
        self.cache[key] = translation
        self.save_cache()
