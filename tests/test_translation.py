import unittest
import os
from src.translation import Translator

class TestTranslation(unittest.TestCase):
    def setUp(self):
        # Initialise translator using local dictionary and a temporary cache file path
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.dict_path = os.path.join(base_dir, 'src', 'translation', 'bilingual_dict.json')
        self.cache_file = os.path.join(base_dir, 'data', 'processed', 'test_translation_cache.json')
        
        self.translator = Translator(dict_path=self.dict_path, cache_file=self.cache_file)

    def tearDown(self):
        # Clean up test cache file if created
        if os.path.exists(self.cache_file):
            try:
                os.remove(self.cache_file)
            except Exception:
                pass

    def test_dictionary_translation_english_to_amharic(self):
        # Test word in dictionary
        translated = self.translator.translate("coffee", source_lang='english', target_lang='amharic')
        self.assertEqual(translated.strip(), "ቡና")

    def test_dictionary_translation_amharic_to_english(self):
        # Test word in dictionary
        translated = self.translator.translate("ቡና", source_lang='amharic', target_lang='english')
        self.assertEqual(translated.strip().lower(), "coffee")

    def test_translation_cache(self):
        # Set cache manually and test retrieve
        self.translator.cache.set("test query", "ሙከራ ጥያቄ", "english", "amharic")
        cached_trans = self.translator.translate("test query", source_lang='english', target_lang='amharic')
        self.assertEqual(cached_trans, "ሙከራ ጥያቄ")

if __name__ == '__main__':
    unittest.main()
