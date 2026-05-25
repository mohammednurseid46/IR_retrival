import unittest
from src.indexing import InvertedIndex
from src.retrieval.tfidf import TFIDF
from src.retrieval.bm25 import BM25

class TestRetrieval(unittest.TestCase):
    def setUp(self):
        self.index = InvertedIndex()
        
        # Add 3 sample documents
        # Doc 1: has "coffee" 2 times
        self.index.add_document("doc1", ["coffee", "ceremony", "coffee", "ethiopia"], {"title": "Doc 1"})
        # Doc 2: has "coffee" 1 time
        self.index.add_document("doc2", ["traditional", "coffee", "cup"], {"title": "Doc 2"})
        # Doc 3: has "ethiopia" 3 times
        self.index.add_document("doc3", ["ethiopia", "history", "ethiopia", "culture", "ethiopia"], {"title": "Doc 3"})

    def test_inverted_index_stats(self):
        self.assertEqual(self.index.num_docs, 3)
        self.assertEqual(self.index.get_doc_freq("coffee"), 2)
        self.assertEqual(self.index.get_doc_freq("history"), 1)
        self.assertEqual(self.index.get_term_tf_in_doc("coffee", "doc1"), 2)

    def test_tfidf_scoring(self):
        tfidf = TFIDF(self.index)
        scores = tfidf.score(["coffee"])
        
        # Both doc1 and doc2 have coffee, doc3 doesn't
        self.assertIn("doc1", scores)
        self.assertIn("doc2", scores)
        self.assertNotIn("doc3", scores)
        
        # Doc 1 has tf = 2/4 = 0.5, Doc 2 has tf = 1/3 = 0.33. Doc 1 score should be higher.
        self.assertGreater(scores["doc1"], scores["doc2"])

    def test_bm25_scoring(self):
        bm25 = BM25(self.index)
        scores = bm25.score(["ethiopia"])
        
        # doc1 and doc3 have "ethiopia"
        self.assertIn("doc1", scores)
        self.assertIn("doc3", scores)
        
        # doc3 has higher frequency of "ethiopia" (3 vs 1)
        self.assertGreater(scores["doc3"], scores["doc1"])

if __name__ == '__main__':
    unittest.main()
