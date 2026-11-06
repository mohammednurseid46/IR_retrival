# Cross-Lingual Information Retrieval (CLIR) System — English ↔ Amharic

This repository implements an end-to-end Cross-Lingual Information Retrieval system that accepts queries in English or Amharic and retrieves ranked documents written in either language. It demonstrates a full pipeline from preprocessing, indexing, and retrieval to an interactive Flask web UI and evaluation reports.

## Highlights

- Language detection and language-specific preprocessing (Amharic normalization)
- Hybrid translation (online translator + bilingual dictionary fallback)
- Inverted index with BM25 and TF-IDF retrieval
- Query expansion and pseudo-relevance feedback (PRF)
- Offline evaluation suite (Precision, Recall, P@K, MAP)
- Live query evaluation in the web UI when a query matches ground-truth

---

## Quickstart

1. Clone and prepare environment:

```bash
git clone <repo-url>
cd CrossLingualIR_AmharicEnglish
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
```

2. Build indexes (scans `data/raw/` → writes to `data/processed/`):

```bash
python run.py --build-index
```

3. Run the web app (default: http://localhost:5000):

```bash
python run.py
```

4. Run offline evaluation (writes `reports/evaluation_results.md`):

```bash
python run.py --evaluate
```

5. Run tests:

```bash
python -m unittest discover tests
```

---

## Database usage

This system does **not** use a database system such as SQLite, PostgreSQL, MySQL, or MongoDB.

Instead, it uses the file system:

- Source documents are read from `data/raw/english/` and `data/raw/amharic/`.
- Processed tokens are saved under `data/processed/`.
- English and Amharic inverted indexes are saved as `data/processed/english_index.json` and `data/processed/amharic_index.json`.
- Document metadata and original document content are saved in `data/metadata/metadata.json`.
- Translation results may be cached in `data/processed/translation_cache.json`.

The indexes and metadata are loaded into memory when the application handles its first search request. Therefore, no database server, database connection, migrations, or database credentials are required.

## How the system works after startup

After running `python run.py`, Flask starts the web application at `http://localhost:5000`. The frontend is served by Flask, so a separate frontend server is not required.

The typical request flow is:

1. The user enters an English or Amharic query in the web interface.
2. The browser sends the query to the Flask `/search` endpoint.
3. The backend detects the query language and preprocesses the query using tokenization, stop-word removal, and normalization.
4. If the query language differs from the target document language, the translator converts the query using the online translator and bilingual dictionary fallback.
5. The backend searches the in-memory English and/or Amharic JSON indexes using BM25 or TF-IDF.
6. Optional query expansion and pseudo-relevance feedback can refine the search query.
7. Results are ranked and returned as JSON, including document title, snippet, language, document ID, and relevance score.
8. The frontend displays the ranked results. Selecting a result requests its full content through `/document/<doc_id>`.
9. The evaluation button sends a `POST` request to `/evaluate`, which runs the evaluation suite and displays the summary metrics.

If the index files do not exist when the application starts, `run.py` automatically builds them before starting Flask. You can also rebuild them explicitly with:

```bash
python run.py --build-index
```

---

## Project layout (important files)

- `run.py` — CLI entrypoint for index building, evaluation, and running the Flask server
- `src/api/app.py`, `src/api/routes.py` — Flask app and endpoints (search, document, evaluate)
- `src/preprocessing/` — `tokenizer.py`, `normalizer.py`, `stopword_remover.py`
- `src/indexing/` — index builder and loader
- `src/retrieval/` — `bm25.py`, `tfidf.py`, `cross_lingual.py` (retriever orchestration)
- `src/evaluation/` — `analyzer.py`, `metrics.py`, `test_queries.json`
- `frontend/` — `templates/` and `static/` (UI assets)

---

## Evaluation details

Ground-truth queries are in `src/evaluation/test_queries.json`. The analyzer (`src/evaluation/analyzer.py`) runs the set of queries under multiple configurations and writes a markdown report to `reports/evaluation_results.md`.

The server also attaches single-query metrics (Precision, Recall, P@1/3/5, AP) to API search responses when the submitted query text exactly matches a ground-truth query, enabling live evaluation in the UI.

---

## Dependencies and optional integrations

See `requirements.txt` for required libraries. Core dependencies include `flask` and `nltk`. Optional advanced enhancements you can add:

- `spaCy` for more advanced tokenization and NER
- `elasticsearch` for a scalable search backend

Example install commands:

```bash
pip install spacy
python -m spacy download en_core_web_sm
pip install elasticsearch
```

---

## Contributing

1. Fork and branch.
2. Run tests and linters.
3. Open a pull request describing your changes.

---

If you'd like, I can add spaCy tokenization or an optional Elasticsearch backend next — tell me which and I'll scaffold it and update `requirements.txt`.
