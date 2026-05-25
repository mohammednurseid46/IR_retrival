import os
import json
import urllib.request
import urllib.parse
from .cache import TranslationCache

class Translator:
    def __init__(self, dict_path=None, cache_file=None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        if not dict_path:
            dict_path = os.path.join(base_dir, 'src', 'translation', 'bilingual_dict.json')
            
        self.dict_path = dict_path
        self.cache = TranslationCache(cache_file)
        self.dictionary = self._load_dictionary()

    def _load_dictionary(self):
        if os.path.exists(self.dict_path):
            try:
                with open(self.dict_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load bilingual dictionary: {e}")
        else:
            print(f"Warning: Bilingual dictionary not found at {self.dict_path}")
        return {"en_to_am": {}, "am_to_en": {}}

    def translate_api(self, text, source_lang, target_lang):
        """Calls a free google translate API endpoint using standard urllib."""
        sl = 'en' if source_lang == 'english' else 'am'
        tl = 'am' if target_lang == 'amharic' else 'en'
        
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={sl}&tl={tl}&dt=t&q={urllib.parse.quote(text)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                # Google single translate format: [[["translated_text", "original_text", ...]]]
                translated_parts = [part[0] for part in data[0] if part[0]]
                return "".join(translated_parts)
        except Exception as e:
            # Silence exceptions, we have fallback dictionary translation
            # print(f"Translation API error: {e}")
            return None

    def translate_dict(self, text, source_lang, target_lang):
        """Falls back to dictionary translation (word-by-word)."""
        words = text.lower().strip().split()
        if not words:
            return ""
            
        direction = "en_to_am" if source_lang == 'english' else "am_to_en"
        vocab = self.dictionary.get(direction, {})
        
        translated_words = []
        for word in words:
            # Strip simple English punctuation
            clean_word = word.strip('.,!?;:()""\'\'')
            if clean_word in vocab:
                # Take the first translation option
                translated_words.append(vocab[clean_word][0])
            else:
                # If not in dictionary, keep the original word
                translated_words.append(word)
                
        return " ".join(translated_words)

    def translate(self, text, source_lang, target_lang):
        """Main translate function checking cache, API, and fallback dictionary."""
        if not text or source_lang == target_lang:
            return text
            
        source_lang = source_lang.lower()
        target_lang = target_lang.lower()
        
        # 1. Check Cache
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached
            
        # 2. Try API
        translated = self.translate_api(text, source_lang, target_lang)
        
        # 3. Fallback to dictionary if API failed
        if not translated:
            translated = self.translate_dict(text, source_lang, target_lang)
            
        # 4. Save to Cache
        if translated:
            self.cache.set(text, translated, source_lang, target_lang)
            
        return translated
