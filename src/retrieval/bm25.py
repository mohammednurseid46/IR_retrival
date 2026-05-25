import math

class BM25:
    def __init__(self, index, k1=1.5, b=0.75):
        self.index = index
        self.k1 = k1
        self.b = b

    def score(self, query_tokens):
        """
        Scores all documents for a given list of query tokens using BM25.
        Returns a dictionary of {doc_id: score}.
        """
        scores = {}
        if not query_tokens:
            return scores
            
        N = self.index.num_docs
        avg_doc_len = self.index.avg_doc_length if self.index.avg_doc_length > 0 else 1.0
        
        for term in query_tokens:
            df = self.index.get_doc_freq(term)
            if df == 0:
                continue
                
            # Compute Robertson-Spärck Jones IDF with smoothing to prevent negative values
            # idf = log(1 + (N - df + 0.5) / (df + 0.5))
            val = (N - df + 0.5) / (df + 0.5)
            # Ensure it is at least a small positive number
            idf = math.log(1.0 + max(0.0001, val))
            
            postings = self.index.index.get(term, {})
            for doc_id, tf in postings.items():
                doc_len = float(self.index.doc_lengths.get(doc_id, 1.0))
                
                # BM25 tf adjustment formula
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / avg_doc_len))
                
                # Update score
                scores[doc_id] = scores.get(doc_id, 0.0) + (idf * (numerator / denominator))
                
        return scores
