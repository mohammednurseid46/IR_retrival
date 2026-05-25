import sys
import os

# Add project root to path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_dir)

from src.language_detection import LanguageDetector
from src.translation import Translator
from src.indexing import InvertedIndex
from src.retrieval import CrossLingualRetriever

detector = LanguageDetector()
en_index = InvertedIndex()
en_index.add_document("english_doc1", ["coffee", "ceremony"], {
    "title": "English Coffee", "snippet": "...", "language": "english", "raw_content": "Coffee ceremony..."
})

am_index = InvertedIndex()
am_index.add_document("amharic_doc1", ["ቡና", "ስርዓት"], {
    "title": "Amharic Coffee", "snippet": "...", "language": "amharic", "raw_content": "የቡና ስርዓት..."
})

indexes = {
    'english': en_index,
    'amharic': am_index
}

dict_path = os.path.join(base_dir, 'src', 'translation', 'bilingual_dict.json')
cache_file = os.path.join(base_dir, 'data', 'processed', 'test_translation_cache.json')

retriever = CrossLingualRetriever(indexes=indexes, dict_path=dict_path, cache_file=cache_file)

print("Detected lang for 'buna':", detector.detect("ቡና"))
trans_api = retriever.translator.translate_api("ቡና", 'amharic', 'english')
print("Translation API returned:", ascii(trans_api))
trans_dict = retriever.translator.translate_dict("ቡና", 'amharic', 'english')
print("Translation Dict returned:", ascii(trans_dict))
final_trans = retriever.translator.translate("ቡና", 'amharic', 'english')
print("Final Translation:", ascii(final_trans))

results = retriever.search("ቡና", target_lang='english')
print("Search results for 'buna' in English index:", results)
