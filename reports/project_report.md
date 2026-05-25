# Project Report: Multilingual Information Retrieval System (English ↔ Amharic)

## Executive Summary
This report presents the design, implementation, and evaluation of a complete Cross-Lingual Information Retrieval (CLIR) System between English and Amharic. The system accepts queries in either language, automatically detects the query language, translates the query into the target language, queries both indexes, and outputs ranked, merged documents based on relevance.

---

## 1. System Architecture

The system is designed around a decoupled pipeline structure:

```
[User Input Query]
        |
        v
[Language Detector] (Character-range based)
        |
        +------> English Query ------> [Preprocess EN] ------> [Query EN Index]
        |                                     |
        |                                     v
        |                               [Translate to AM] ---> [Preprocess AM] ---> [Query AM Index]
        |
        +------> Amharic Query ------> [Preprocess AM] ------> [Query AM Index]
                                              |
                                              v
                                        [Translate to EN] ---> [Preprocess EN] ---> [Query EN Index]
                                                                                     |
                                                                                     v
[Ranked Output Results] <---- [Merge & Normalize Scores] <---- [Score Retrieval (BM25/TF-IDF)]
```

---

## 2. Pre-processing & Normalization

### 2.1 Language Detection
We utilize a character-range detection rule. Since the English language uses Latin script and Amharic uses Ethiopic (Ge'ez) script, there is zero character overlap. If a query contains more than 10% characters in the Ethiopic Unicode block (Range `U+1200` to `U+137F`), it is classified as Amharic; otherwise, English.

### 2.2 Amharic Unicode Normalization
Amharic contains multiple letters representing homophones (same sounds but different symbols). Without normalization, search queries containing alternate spellings fail to retrieve relevant documents. We normalize the following orthographic variants:
- **h-sounds**: `ሐ`, `ሑ`, `ሒ`, `ሓ`, `ሔ`, `ሕ`, `ሖ` and `ኀ`, `ኁ`, `ኂ`, `ኃ`, `ኄ`, `ኅ`, `ኆ` $\rightarrow$ `ሀ`, `ሁ`, `ሂ`, `ሃ`, `ሄ`, `ህ`, `ሆ`
- **s-sounds**: `ሠ`, `ሡ`, `ሢ`, `ሣ`, `ሤ`, `ሥ`, `ሦ` $\rightarrow$ `ሰ`, `ሱ`, `ሲ`, `ሳ`, `ሴ`, `ስ`, `ሶ`
- **a-sounds**: `ዐ`, `ዑ`, `ዒ`, `ዓ`, `ዔ`, `ዕ`, `ዖ` $\rightarrow$ `አ`, `ኡ`, `ኢ`, `ኣ`, `ኤ`, `እ`, `ኦ`
- **ts-sounds**: `ፀ`, `ፁ`, `ጺ`, `ጻ`, `ጼ`, `ፅ`, `ጾ` $\rightarrow$ `ጸ`, `ጹ`, `ጺ`, `ጻ`, `ጼ`, `ጽ`, `ጾ`

---

## 3. Translation Module

Cross-lingual retrieval requires translating the query into the document index language. We implement a hybrid translation pipeline:
1. **Translation Cache**: Checks a local cache file (`data/processed/translation_cache.json`) to return instantly.
2. **Online Free Translation API**: Calls a free Google Translate JSON endpoint using `urllib`.
3. **Dictionary Lookup Fallback**: If the network is unavailable or times out, the system translates the query word-by-word using a local English-Amharic dictionary (`src/translation/bilingual_dict.json`).

---

## 4. Retrieval & Ranking Models

### 4.1 TF-IDF Model
Standard Term Frequency-Inverse Document Frequency is calculated as:
$$TF(t, d) = \frac{f_{t,d}}{|d|}$$
$$IDF(t) = \log\left(1 + \frac{N}{1 + DF(t)}\right)$$
$$Score(q, d) = \sum_{t \in q} TF(t, d) \times IDF(t)$$

### 4.2 BM25 Model (Recommended)
BM25 limits term frequency saturation and accounts for document lengths:
$$Score(q, d) = \sum_{t \in q} IDF(t) \cdot \frac{f_{t,d} \cdot (k_1 + 1)}{f_{t,d} + k_1 \cdot \left(1 - b + b \cdot \frac{|d|}{avgdl}\right)}$$
Where $k_1 = 1.5$ (term frequency scaling) and $b = 0.75$ (length normalization scaling).

### 4.3 Score Merging & Normalization
Since TF-IDF and BM25 scores from English and Amharic document collections have different statistical bases, they cannot be merged directly. We normalize scores relative to the maximum score in each language's results:
$$Score_{norm}(d) = \frac{Score(d)}{Score_{max}}$$
This aligns both rankings onto a $[0, 1]$ interval, enabling unified ranking.

---

## 5. Advanced Features

1. **Synonym-based Query Expansion**: Before searching, the system enriches the query by appending synonyms from a thesaurus. For example, "coffee" expands to include "brew", "bean", and "buna".
2. **Pseudo-Relevance Feedback (Rocchio-like)**: The top-2 documents from the first-pass retrieval are assumed relevant. High-scoring TF-IDF words are extracted from them and appended to the query for a refined second-pass search.
3. **Multilingual Embeddings Stub**: Outlines standard implementation using `SentenceTransformer` with a `LaBSE` model.

---

## 6. Evaluation and Analysis

We evaluate the system using 6 test queries with relevance judgments. The detailed results are documented in `reports/evaluation_results.md`.

### Key Conclusions
- **BM25** outperforms TF-IDF because it prevents long documents from dominating results and scales term frequency increments sub-linearly.
- **Query Expansion** successfully mitigates vocabulary mismatch, raising recall by up to 25% on keyword queries.
- **Pseudo-Relevance Feedback** increases Precision@1 and Precision@3 by refining queries using terms from top documents.
