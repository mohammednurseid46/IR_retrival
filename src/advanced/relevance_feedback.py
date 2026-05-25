class RelevanceFeedback:
    def __init__(self, index):
        self.index = index

    def get_feedback_terms(self, top_doc_ids, query_tokens, num_terms=3):
        """
        Extracts top terms from a set of relevant documents (excluding original query terms)
        to expand the search query (Pseudo-Relevance Feedback).
        """
        if not top_doc_ids:
            return []

        term_scores = {}
        
        # Calculate term frequencies in the feedback documents
        for doc_id in top_doc_ids:
            # Look in the index to see which terms appear in this document
            for term, postings in self.index.index.items():
                if doc_id in postings:
                    # Ignore terms that are already part of the query
                    if term in query_tokens:
                        continue
                        
                    tf = postings[doc_id]
                    df = self.index.get_doc_freq(term)
                    
                    # Compute a TF-IDF weight for the term in the relevant document
                    # More frequent in these documents, and less frequent globally
                    # Weight = tf * log(1 + N / df)
                    import math
                    N = self.index.num_docs
                    idf = math.log(1 + (N / (1 + df)))
                    
                    term_scores[term] = term_scores.get(term, 0.0) + (tf * idf)

        # Sort terms by their score
        sorted_terms = sorted(term_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top N feedback terms
        return [term for term, score in sorted_terms[:num_terms]]
