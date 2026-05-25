import math

class TFIDF:
    def __init__(self, index):
        self.index = index

    def score(self, query_tokens):
        """
        Scores all documents for a given list of query tokens using TF-IDF.
        Returns a dictionary of {doc_id: score}.
        """
        scores = {}
        if not query_tokens:
            return scores
            
        N = self.index.num_docs
        
        for term in query_tokens:
            df = self.index.get_doc_freq(term)
            if df == 0:
                continue
                
            # Compute IDF: log(1 + N / df)
            # Add 1 to numerator and denominator to avoid log(0) and division by zero
            idf = math.log(1 + (N / (1 + df)))
            
            # Find documents containing this term
            postings = self.index.index.get(term, {})
            for doc_id, tf in postings.items():
                doc_len = float(self.index.doc_lengths.get(doc_id, 1.0))
                # Normalized TF: tf / doc_len
                norm_tf = tf / doc_len
                
                # Update score
                scores[doc_id] = scores.get(doc_id, 0.0) + (norm_tf * idf)
                
        return scores
