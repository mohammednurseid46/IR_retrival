import os

class MultilingualEmbeddingsRetriever:
    def __init__(self, metadata_path=None):
        self.enabled = False
        self.model = None
        self.corpus_embeddings = None
        self.doc_ids = []
        
        # Check if sentence-transformers is installed
        try:
            from sentence_transformers import SentenceTransformer, util
            import torch
            self.SentenceTransformer = SentenceTransformer
            self.util = util
            self.torch = torch
            self.enabled = True
        except ImportError:
            # sentence-transformers not installed
            pass

    def initialize_model(self, model_name='sentence-transformers/LaBSE'):
        """Initializes the multilingual embedding model (e.g. LaBSE)."""
        if not self.enabled:
            return False
            
        try:
            # LaBSE is a multilingual BERT model supporting English and Amharic
            self.model = self.SentenceTransformer(model_name)
            return True
        except Exception as e:
            print(f"Error loading multilingual model: {e}")
            self.enabled = False
            return False

    def index_documents(self, documents):
        """
        Embeds a list of documents (dictionaries containing 'doc_id' and 'raw_content').
        """
        if not self.enabled or not self.model:
            return False
            
        try:
            self.doc_ids = [doc['doc_id'] for doc in documents]
            texts = [doc['raw_content'] for doc in documents]
            
            # Compute embeddings
            self.corpus_embeddings = self.model.encode(texts, convert_to_tensor=True)
            return True
        except Exception as e:
            print(f"Error embedding documents: {e}")
            return False

    def search(self, query_text, top_k=5):
        """
        Retrieves top_k documents for query_text using embedding cosine similarity.
        """
        if not self.enabled or self.model is None or self.corpus_embeddings is None:
            return None # Fallback indicator
            
        try:
            query_embedding = self.model.encode(query_text, convert_to_tensor=True)
            cos_scores = self.util.cos_sim(query_embedding, self.corpus_embeddings)[0]
            
            # Sort scores
            top_results = self.torch.topk(cos_scores, k=min(top_k, len(self.doc_ids)))
            
            results = []
            for score, idx in zip(top_results[0], top_results[1]):
                doc_idx = int(idx)
                results.append({
                    'doc_id': self.doc_ids[doc_idx],
                    'score': float(score)
                })
            return results
        except Exception as e:
            print(f"Error during embedding search: {e}")
            return None
