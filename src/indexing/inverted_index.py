import json
import os

class InvertedIndex:
    def __init__(self):
        # term -> {doc_id: tf}
        self.index = {}
        # doc_id -> length (number of tokens)
        self.doc_lengths = {}
        # doc_id -> metadata (title, file path, language, snippet)
        self.doc_metadata = {}
        # Total number of documents in index
        self.num_docs = 0
        # Average document length in this index
        self.avg_doc_length = 0.0

    def add_document(self, doc_id, tokens, metadata):
        """Adds a document's tokens to the inverted index."""
        if not tokens:
            return
            
        doc_len = len(tokens)
        self.doc_lengths[doc_id] = doc_len
        self.doc_metadata[doc_id] = metadata
        self.num_docs += 1
        
        # Count term frequencies in this document
        tf_dict = {}
        for token in tokens:
            tf_dict[token] = tf_dict.get(token, 0) + 1
            
        # Update inverted index
        for term, tf in tf_dict.items():
            if term not in self.index:
                self.index[term] = {}
            self.index[term][doc_id] = tf
            
        # Recompute average doc length
        total_len = sum(self.doc_lengths.values())
        self.avg_doc_length = total_len / self.num_docs

    def get_doc_freq(self, term):
        """Returns document frequency (df) for a term."""
        if term in self.index:
            return len(self.index[term])
        return 0

    def get_term_tf_in_doc(self, term, doc_id):
        """Returns term frequency (tf) of a term in a document."""
        if term in self.index and doc_id in self.index[term]:
            return self.index[term][doc_id]
        return 0

    def save(self, file_path):
        """Saves the index data to a JSON file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        data = {
            'index': self.index,
            'doc_lengths': self.doc_lengths,
            'doc_metadata': self.doc_metadata,
            'num_docs': self.num_docs,
            'avg_doc_length': self.avg_doc_length
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, file_path):
        """Loads index data from a JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Index file not found at {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.index = data.get('index', {})
        self.doc_lengths = data.get('doc_lengths', {})
        self.doc_metadata = data.get('doc_metadata', {})
        self.num_docs = data.get('num_docs', 0)
        self.avg_doc_length = data.get('avg_doc_length', 0.0)
