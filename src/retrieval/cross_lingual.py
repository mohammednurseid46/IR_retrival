import os
from src.language_detection import LanguageDetector
from src.translation import Translator
from src.preprocessing import Tokenizer, StopwordRemover, Normalizer
from src.indexing import IndexLoader
from .tfidf import TFIDF
from .bm25 import BM25
from .ranker import Ranker

class CrossLingualRetriever:
    def __init__(self, indexes=None, dict_path=None, cache_file=None):
        # Load indexes if not provided
        if not indexes:
            try:
                self.indexes = IndexLoader.load_both_indexes()
            except Exception as e:
                print(f"Warning: Could not load indexes automatically: {e}")
                self.indexes = {}
        else:
            self.indexes = indexes

        self.detector = LanguageDetector()
        self.translator = Translator(dict_path=dict_path, cache_file=cache_file)
        
        self.tokenizer = Tokenizer()
        self.stopword_remover = StopwordRemover()
        self.normalizer = Normalizer()

    def search(self, query_text, method='bm25', target_lang='both', k1=1.5, b=0.75):
        """
        Main cross-lingual search interface.
        - query_text: The user's raw query (English or Amharic)
        - method: 'bm25' or 'tfidf'
        - target_lang: 'english', 'amharic', or 'both' (merged)
        """
        if not query_text or not self.indexes:
            return []

        # 1. Detect query language
        query_lang = self.detector.detect(query_text)
        
        results = {}

        # Preprocess helper
        def get_preprocessed_tokens(text, lang):
            tokens = self.tokenizer.tokenize(text, language=lang)
            tokens = self.stopword_remover.remove_stopwords(tokens, language=lang)
            return [self.normalizer.normalize(t, language=lang) for t in tokens if t]

        # 2. Retrieve English documents
        if target_lang in ['english', 'both'] and 'english' in self.indexes:
            # Determine search query for English index
            if query_lang == 'english':
                search_query = query_text
            else:
                # Translate Amharic query to English
                search_query = self.translator.translate(query_text, source_lang='amharic', target_lang='english')
                
            en_tokens = get_preprocessed_tokens(search_query, 'english')
            
            # Score English documents
            index_en = self.indexes['english']
            scorer = BM25(index_en, k1=k1, b=b) if method == 'bm25' else TFIDF(index_en)
            en_scores = scorer.score(en_tokens)
            
            # Normalize English scores
            if en_scores:
                max_en = max(en_scores.values())
                for doc_id, score in en_scores.items():
                    results[doc_id] = (score / max_en) if max_en > 0 else 0.0

        # 3. Retrieve Amharic documents
        if target_lang in ['amharic', 'both'] and 'amharic' in self.indexes:
            # Determine search query for Amharic index
            if query_lang == 'amharic':
                search_query = query_text
            else:
                # Translate English query to Amharic
                search_query = self.translator.translate(query_text, source_lang='english', target_lang='amharic')
                
            am_tokens = get_preprocessed_tokens(search_query, 'amharic')
            
            # Score Amharic documents
            index_am = self.indexes['amharic']
            scorer = BM25(index_am, k1=k1, b=b) if method == 'bm25' else TFIDF(index_am)
            am_scores = scorer.score(am_tokens)
            
            # Normalize Amharic scores
            if am_scores:
                max_am = max(am_scores.values())
                for doc_id, score in am_scores.items():
                    results[doc_id] = (score / max_am) if max_am > 0 else 0.0

        # 4. Rank merged results
        ranked = Ranker.rank_results(results)
        
        # Build response structure with metadata
        output = []
        for doc_id, score in ranked:
            lang = 'english' if doc_id.startswith('english') else 'amharic'
            meta = self.indexes[lang].doc_metadata[doc_id]
            output.append({
                'doc_id': doc_id,
                'score': score,
                'title': meta['title'],
                'snippet': meta['snippet'],
                'language': meta['language'],
                'raw_content': meta['raw_content']
            })
            
        return output
