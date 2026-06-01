from flask import Blueprint, request, jsonify, render_template
from src.retrieval import CrossLingualRetriever
from src.advanced.query_expansion import QueryExpander
from src.advanced.relevance_feedback import RelevanceFeedback
from src.evaluation import EvaluationAnalyzer
import os

api_blueprint = Blueprint('api', __name__)

# Initialize Retriever lazily to prevent errors if indexes are not built yet
retriever = None

def get_retriever():
    global retriever
    if retriever is None:
        retriever = CrossLingualRetriever()
    return retriever

@api_blueprint.route('/')
def home():
    return render_template('index.html')

@api_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    method = request.args.get('method', 'bm25').lower()
    target_lang = request.args.get('target_lang', 'both').lower()
    use_expansion = request.args.get('expand', 'false').lower() == 'true'
    use_feedback = request.args.get('feedback', 'false').lower() == 'true'

    if not query:
        return jsonify({'results': [], 'query_detected': 'unknown', 'query_used': ''})

    try:
        r = get_retriever()
        
        # 1. Detect language
        query_lang = r.detector.detect(query)
        
        search_query = query
        expansion_terms = []
        feedback_terms = []

        # 2. Advanced Feature: Query Expansion
        if use_expansion:
            expander = QueryExpander()
            # Tokenize & remove stopwords to find expansion terms
            tokens = r.tokenizer.tokenize(query, language=query_lang)
            tokens = r.stopword_remover.remove_stopwords(tokens, language=query_lang)
            expanded_tokens = expander.expand(tokens, language=query_lang)
            
            # Find which terms are new
            expansion_terms = [t for t in expanded_tokens if t not in tokens]
            if expansion_terms:
                search_query = query + " " + " ".join(expansion_terms)

        # 3. Perform initial search
        results = r.search(search_query, method=method, target_lang=target_lang)

        # 4. Advanced Feature: Pseudo-Relevance Feedback (Rocchio)
        if use_feedback and results and len(results) > 0:
            # Assume top 2 documents are relevant
            top_docs = [res['doc_id'] for res in results[:2]]
            
            # Use index of the query language (or both) to find feedback terms
            lang_index = r.indexes.get(query_lang)
            if lang_index:
                rf = RelevanceFeedback(lang_index)
                query_tokens = r.tokenizer.tokenize(search_query, language=query_lang)
                feedback_terms = rf.get_feedback_terms(top_docs, query_tokens, num_terms=2)
                
                if feedback_terms:
                    # Append feedback terms and perform search again
                    search_query = search_query + " " + " ".join(feedback_terms)
                    results = r.search(search_query, method=method, target_lang=target_lang)

        # Attach query-level evaluation if the query has a ground-truth judgment
        evaluation = None
        try:
            analyzer = EvaluationAnalyzer()
            evaluation = analyzer.evaluate_single_query(query, results)
        except Exception:
            evaluation = None

        return jsonify({
            'results': results,
            'query_detected': query_lang,
            'query_used': search_query,
            'expansion_terms': expansion_terms,
            'feedback_terms': feedback_terms,
            'evaluation': evaluation
        })

    except Exception as e:
        return jsonify({'error': str(e), 'results': []}), 500

@api_blueprint.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('q', '').strip()
    method = request.args.get('method', 'bm25').lower()
    target_lang = request.args.get('target_lang', 'both').lower()
    use_expansion = request.args.get('expand', 'false').lower() == 'true'
    
    results = []
    if query:
        try:
            r = get_retriever()
            query_lang = r.detector.detect(query)
            search_query = query
            if use_expansion:
                expander = QueryExpander()
                tokens = r.tokenizer.tokenize(query, language=query_lang)
                tokens = r.stopword_remover.remove_stopwords(tokens, language=query_lang)
                expanded = expander.expand(tokens, language=query_lang)
                search_query = " ".join(expanded)
            results = r.search(search_query, method=method, target_lang=target_lang)
        except Exception as e:
            print(f"Error in search_results: {e}")
            
    return render_template('results.html', query=query, results=results, method=method)

@api_blueprint.route('/document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    try:
        r = get_retriever()
        lang = 'english' if doc_id.startswith('english') else 'amharic'
        if lang in r.indexes and doc_id in r.indexes[lang].doc_metadata:
            meta = r.indexes[lang].doc_metadata[doc_id]
            return jsonify({
                'doc_id': doc_id,
                'title': meta['title'],
                'language': meta['language'],
                'content': meta['raw_content']
            })
        return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/evaluate', methods=['POST'])
def run_evaluation():
    try:
        analyzer = EvaluationAnalyzer()
        results = analyzer.run_analysis()
        # Return summary configuration metrics
        summary = {name: data['summary'] for name, data in results.items()}
        return jsonify({'status': 'success', 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
