class Ranker:
    @staticmethod
    def rank_results(scores):
        """
        Takes a dict of {doc_id: score} and returns a sorted list of tuples (doc_id, score) 
        in descending order of relevance.
        """
        if not scores:
            return []
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
