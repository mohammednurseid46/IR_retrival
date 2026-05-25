import os
import json
from src.preprocessing import Tokenizer, StopwordRemover, Normalizer
from .inverted_index import InvertedIndex

class IndexBuilder:
    def __init__(self, data_dir=None):
        if not data_dir:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            data_dir = os.path.join(base_dir, 'data')
            
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, 'raw')
        self.processed_dir = os.path.join(data_dir, 'processed')
        self.metadata_dir = os.path.join(data_dir, 'metadata')
        
        # Intermediate output dirs
        self.tokenized_dir = os.path.join(self.processed_dir, 'tokenized')
        self.stopwords_removed_dir = os.path.join(self.processed_dir, 'stopwords_removed')
        self.normalized_dir = os.path.join(self.processed_dir, 'normalized')

        self.tokenizer = Tokenizer()
        self.stopword_remover = StopwordRemover()
        self.normalizer = Normalizer()

    def build_indexes(self):
        """Scans raw directories, preprocesses, and builds inverted indexes for English and Amharic."""
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        languages = ['english', 'amharic']
        indexes = {
            'english': InvertedIndex(),
            'amharic': InvertedIndex()
        }
        
        all_metadata = {}

        for lang in languages:
            lang_raw_dir = os.path.join(self.raw_dir, lang)
            if not os.path.exists(lang_raw_dir):
                print(f"Warning: Raw directory for {lang} not found at {lang_raw_dir}. Skipping.")
                continue

            # Ensure processed subdirs exist for this language
            os.makedirs(os.path.join(self.tokenized_dir, lang), exist_ok=True)
            os.makedirs(os.path.join(self.stopwords_removed_dir, lang), exist_ok=True)
            os.makedirs(os.path.join(self.normalized_dir, lang), exist_ok=True)

            print(f"Processing {lang} documents...")
            
            # Read files in raw directory
            filenames = [f for f in os.listdir(lang_raw_dir) if f.endswith('.txt')]
            for filename in filenames:
                file_path = os.path.join(lang_raw_dir, filename)
                doc_id = f"{lang}_{os.path.splitext(filename)[0]}"
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_content = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue

                # Title can be derived from filename or first line
                title = f"{lang.capitalize()} Document - {filename}"
                first_line = raw_content.strip().split('\n')[0]
                if len(first_line) < 60:
                    title = first_line

                # 1. Tokenize
                tokens = self.tokenizer.tokenize(raw_content, language=lang)
                self._save_tokens(tokens, os.path.join(self.tokenized_dir, lang, filename))

                # 2. Remove Stopwords
                tokens_no_stop = self.stopword_remover.remove_stopwords(tokens, language=lang)
                self._save_tokens(tokens_no_stop, os.path.join(self.stopwords_removed_dir, lang, filename))

                # 3. Normalize / Stem
                normalized_tokens = [self.normalizer.normalize(tok, language=lang) for tok in tokens_no_stop]
                # Filter out empty or very short tokens resulting from normalization if any
                normalized_tokens = [tok for tok in normalized_tokens if tok]
                self._save_tokens(normalized_tokens, os.path.join(self.normalized_dir, lang, filename))

                # Snippet (first 150 chars)
                snippet = raw_content[:150] + "..." if len(raw_content) > 150 else raw_content

                metadata = {
                    'doc_id': doc_id,
                    'title': title,
                    'filename': filename,
                    'language': lang,
                    'file_path': file_path,
                    'snippet': snippet,
                    'raw_content': raw_content
                }
                
                all_metadata[doc_id] = metadata
                
                # Add to index
                indexes[lang].add_document(doc_id, normalized_tokens, metadata)

        # Save metadata
        metadata_file = os.path.join(self.metadata_dir, 'metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(all_metadata, f, ensure_ascii=False, indent=2)
        print(f"Metadata saved to {metadata_file}")

        # Save indexes
        for lang, index in indexes.items():
            index_path = os.path.join(self.processed_dir, f"{lang}_index.json")
            index.save(index_path)
            print(f"Saved {lang} inverted index containing {index.num_docs} documents to {index_path}")

    def _save_tokens(self, tokens, file_path):
        """Helper to write space-separated tokens to a file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(" ".join(tokens))
