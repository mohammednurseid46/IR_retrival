# Cross-Lingual Information Retrieval (CLIR) System (English ↔ Amharic)

A complete, end-to-end Multilingual Information Retrieval system built in Python using Flask for the web interface. The system allows users to query in one language (English or Amharic) and retrieve ranked, relevant documents written in either language (monolingual and cross-lingual search).

---

## Key Features

1. **Robust Text Pre-processing**:
   - **Language Detection**: Custom character-based unicode range detector (100% accurate because Latin and Ge'ez alphabets do not overlap).
   - **Tokenization**: Standard word split for English; Ethiopic punctuation and separator handling (`፡`, `።`, `፣`, `፤`) for Amharic.
   - **Stopword Removal**: Fully customizable English and Amharic stopword lists.
   - **Normalization**: Collapsing homophones in Amharic (e.g., merging spelling variations of `h`, `s`, `a`, `ts` sounds) to resolve lexical variations, and simple suffix stemming.

2. **Advanced Translation Module**:
   - **Google Translate API integration**: Online free translating API calls.
   - **Bilingual Dictionary Fallback**: Pre-built dictionary in `src/translation/bilingual_dict.json` to enable search even when offline.
   - **Translation Caching**: Local JSON disk cache to store translations and speed up repetitive queries.

3. **Custom Indexing & Retrieval Engine**:
   - **Inverted Index**: Term-frequencies, postings list, document lengths, and metadata.
   - **Dual Model Support**: High-performance **BM25** (with customizable $k_1$ and $b$) and standard **TF-IDF** scoring models.
   - **Score Normalization**: Ensures that retrieval scores from different languages' indexes are merged fairly before joint ranking.

4. **Advanced Retrieval Features**:
   - **Query Expansion**: Enriches queries with thesaurus-based synonyms in both languages before retrieval.
   - **Pseudo-Relevance Feedback (PRF)**: Implements a Rocchio-like feedback loop which takes top retrieved documents, extracts high tf-idf expansion terms, and executes a second-pass search.
   - **Multilingual Embeddings (LaBSE)**: Code-level stub showing how to plug in Sentence-Transformers for dense multilingual retrieval.

5. **Modern Web UI**:
   - **Aesthetic**: Premium dark mode, radial glow gradients, glassmorphism cards, interactive badges.
   - **Interactivity**: Dynamic AJAX searching with detected language badges, instant document expansion modal, and an interactive evaluation runner.

---

## Directory Structure

```
├── data/
│   ├── raw/                      # Original collected documents
│   │   ├── english/              # 12 English documents
│   │   └── amharic/              # 12 Amharic documents
│   ├── processed/                # Intermediate preprocessed files and indexes
│   ├── stopwords/                # Stopword lists
│   └── metadata/                 # metadata.json
├── src/                          # System modules
│   ├── preprocessing/            # Tokenization, Normalization, Stopwords
│   ├── language_detection/       # Unicode block ranges, Language detection
│   ├── translation/              # Hybrid Translation, Dictionary, Cache
│   ├── indexing/                 # Inverted Index, Builder, Loader
│   ├── retrieval/                # TF-IDF, BM25, Cross-Lingual Search, Ranker
│   ├── advanced/                 # Query Expansion, PRF, LaBSE Embeddings
│   ├── evaluation/               # Metrics (P, R, P@K, MAP), Analyzer
│   ├── api/                      # Flask App, Routes, Data Models
│   └── utils/                    # File Handlers, Logger
├── frontend/                     # Web pages & assets
│   ├── templates/                # index.html, results.html
│   └── static/                   # CSS (style.css), JS (main.js)
├── tests/                        # Automated unit tests
├── notebooks/                    # Experimentation notebooks
└── reports/                      # Evaluation and Dataset reports
```

---

## Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build Inverted Indexes
This scans all documents in `data/raw/`, processes them (tokenizes, filters stopwords, normalizes), generates intermediate processed files, and writes the indexes to `data/processed/`:
```bash
python run.py --build-index
```

### 3. Run System Evaluations
This runs our suite of 6 ground-truth test queries, computes macro-averaged Precision, Recall, Precision@K, and MAP across configurations (TF-IDF vs BM25 vs Query Expansion), and outputs a report in `reports/evaluation_results.md`:
```bash
python run.py --evaluate
```

### 4. Run the Web Application
To launch the Flask search interface:
```bash
python run.py
```
Open [http://localhost:5000](http://localhost:5000) in your web browser to start searching!

---

## Running Unit Tests
We have built unit tests covering tokenization, normalization, bilingual dictionary lookup, translation cache, scoring formulas, and retriever routing. Run them with:
```bash
python -m unittest discover tests
```
