import unittest
import os
from src.language_detection import LanguageDetector
from src.retrieval import CrossLingualRetriever
from src.indexing import InvertedIndex

class TestCrossLingual(unittest.TestCase):
    def setUp(self):
        self.detector = LanguageDetector()
        
        # Build mini mock indexes
        self.en_index = InvertedIndex()
        self.en_index.add_document("english_doc1", ["coffee", "ceremony"], {
            "title": "English Coffee", "snippet": "...", "language": "english", "raw_content": "Coffee ceremony..."
        })
        
        self.am_index = InvertedIndex()
        self.am_index.add_document("amharic_doc1", ["ቡና", "ስርዓት"], {
            "title": "Amharic Coffee", "snippet": "...", "language": "amharic", "raw_content": "የቡና ስርዓት..."
        })
        
        self.indexes = {
            'english': self.en_index,
            'amharic': self.am_index
        }
        
        # Load local bilingual dictionary path
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dict_path = os.path.join(base_dir, 'src', 'translation', 'bilingual_dict.json')
        
        self.retriever = CrossLingualRetriever(indexes=self.indexes, dict_path=dict_path)

    def test_language_detection(self):
        # English detection
        self.assertEqual(self.detector.detect("Ethiopian coffee is delicious"), "english")
        self.assertEqual(self.detector.detect("Addis Ababa city"), "english")
        
        # Amharic detection (using Ethiopic range characters)
        self.assertEqual(self.detector.detect("የቡና ሥነ ሥርዓት"), "amharic")
        self.assertEqual(self.detector.detect("አዲስ አበባ ከተማ"), "amharic")

    def test_cross_lingual_retrieval(self):
        # English query should retrieve Amharic document by translating "coffee" -> "ቡና"
        results = self.retriever.search("coffee", target_lang='amharic')
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['doc_id'], "amharic_doc1")
        
        # Amharic query should retrieve English document by translating "ቡና" -> "coffee"
        results2 = self.retriever.search("ቡና", target_lang='english')
        self.assertTrue(len(results2) > 0)
        self.assertEqual(results2[0]['doc_id'], "english_doc1")

if __name__ == '__main__':
    unittest.main()
