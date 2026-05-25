import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.retrieval.cross_lingual import CrossLingualRetriever

if __name__ == '__main__':
    r = CrossLingualRetriever()
    print('Loaded indexes:', list(r.indexes.keys()))
    print('\nSearch: Bahir Dar University (English query)')
    en_results = r.search('Bahir Dar University', method='bm25', target_lang='both')
    for res in en_results[:5]:
        print(res['doc_id'], res['language'], res['score'])
    
    print('\nSearch: ባህር ዳር ዩኒቨርሲቲ (Amharic query)')
    am_results = r.search('ባህር ዳር ዩኒቨርሲቲ', method='bm25', target_lang='both')
    for res in am_results[:5]:
        print(res['doc_id'], res['language'], res['score'])
