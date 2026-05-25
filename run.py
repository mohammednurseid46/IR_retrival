import os
import sys
import argparse
from src.indexing import IndexBuilder
from src.api.app import create_app
from src.evaluation import EvaluationAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Cross-Lingual Information Retrieval (CLIR) System")
    parser.add_argument('--build-index', action='store_true', help="Rebuild inverted indexes from raw data")
    parser.add_argument('--evaluate', action='store_true', help="Run evaluation suite and exit")
    parser.add_argument('--port', type=int, default=5000, help="Port to run Flask server on")
    args = parser.parse_args()

    # 1. Self-indexing check
    base_dir = os.path.dirname(os.path.abspath(__file__))
    en_index_path = os.path.join(base_dir, 'data', 'processed', 'english_index.json')
    am_index_path = os.path.join(base_dir, 'data', 'processed', 'amharic_index.json')

    index_exists = os.path.exists(en_index_path) and os.path.exists(am_index_path)

    if args.build_index or not index_exists:
        print("Indexes not found or --build-index flag passed. Starting index builder pipeline...")
        builder = IndexBuilder()
        builder.build_indexes()
        print("Index building completed successfully!\n")

    # 2. Evaluation check
    if args.evaluate:
        print("Running evaluation suite...")
        analyzer = EvaluationAnalyzer()
        analyzer.run_analysis()
        print("Evaluation completed! Report saved to reports/evaluation_results.md.")
        sys.exit(0)

    # 3. Boot Flask App
    print("Starting Flask Web Application...")
    app = create_app()
    app.run(host='0.0.0.0', port=args.port, debug=True)

if __name__ == '__main__':
    main()
