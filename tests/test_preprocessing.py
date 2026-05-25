import unittest
from src.preprocessing import Tokenizer, StopwordRemover, Normalizer

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()
        self.stopword_remover = StopwordRemover()
        self.normalizer = Normalizer()

    def test_english_tokenization(self):
        text = "Coffee, from Ethiopia's Kaffa region!"
        tokens = self.tokenizer.tokenize(text, language='english')
        self.assertEqual(tokens, ["coffee", "from", "ethiopia", "s", "kaffa", "region"])

    def test_amharic_tokenization(self):
        text = "ቡና፡ለዓለም፡የቀረበ።"
        tokens = self.tokenizer.tokenize(text, language='amharic')
        self.assertEqual(tokens, ["ቡና", "ለዓለም", "የቀረበ"])

    def test_stopword_removal(self):
        tokens = ["the", "coffee", "is", "good", "and", "delicious"]
        filtered = self.stopword_remover.remove_stopwords(tokens, language='english')
        # 'the', 'is', 'and' are stopwords
        self.assertNotIn("the", filtered)
        self.assertNotIn("is", filtered)
        self.assertNotIn("and", filtered)
        self.assertIn("coffee", filtered)

    def test_amharic_normalization(self):
        # 'ሐገር' should normalize to 'ሀገር' (ሐ -> ሀ)
        # 'አዲሥ' should normalize to 'አዲስ' (ሥ -> ስ)
        self.assertEqual(self.normalizer.normalize("ሐገር", 'amharic'), "ሀገር")
        self.assertEqual(self.normalizer.normalize("አዲሥ", 'amharic'), "አዲስ")
        self.assertEqual(self.normalizer.normalize("ፀሐይ", 'amharic'), "ጸሀይ")

if __name__ == '__main__':
    unittest.main()
