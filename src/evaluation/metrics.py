class Metrics:
    @staticmethod
    def precision(retrieved, relevant):
        """
        Calculates standard Precision.
        - retrieved: list of retrieved doc IDs
        - relevant: set of relevant doc IDs
        """
        if not retrieved:
            return 0.0
            
        retrieved_set = set(retrieved)
        intersection = retrieved_set.intersection(relevant)
        return len(intersection) / len(retrieved)

    @staticmethod
    def recall(retrieved, relevant):
        """
        Calculates standard Recall.
        - retrieved: list of retrieved doc IDs
        - relevant: set of relevant doc IDs
        """
        if not relevant:
            return 1.0 # If no relevant docs exist, recall is trivially 1.0
            
        retrieved_set = set(retrieved)
        intersection = retrieved_set.intersection(relevant)
        return len(intersection) / len(relevant)

    @staticmethod
    def precision_at_k(retrieved, relevant, k):
        """
        Calculates Precision@K.
        - retrieved: list of retrieved doc IDs
        - relevant: set of relevant doc IDs
        - k: cutoff rank
        """
        if not retrieved or k <= 0:
            return 0.0
            
        top_k = retrieved[:k]
        intersection = set(top_k).intersection(relevant)
        return len(intersection) / k

    @staticmethod
    def average_precision(retrieved, relevant):
        """
        Calculates Average Precision (AP) for a single query.
        """
        if not relevant:
            return 0.0
            
        ap_sum = 0.0
        relevant_retrieved_count = 0
        
        for idx, doc_id in enumerate(retrieved):
            if doc_id in relevant:
                relevant_retrieved_count += 1
                # Precision at the rank of this relevant document
                prec_at_rank = relevant_retrieved_count / (idx + 1)
                ap_sum += prec_at_rank
                
        return ap_sum / len(relevant)
