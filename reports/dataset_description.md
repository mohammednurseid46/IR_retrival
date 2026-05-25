# Dataset Description

This document describes the dataset collected for the English-Amharic Cross-Lingual Information Retrieval (CLIR) System.

## Overview
The dataset contains a total of **24 documents**:
- **12 English documents** (stored in `data/raw/english/`)
- **12 Amharic documents** (stored in `data/raw/amharic/`)

The documents represent high-quality text collected from news outlets, educational materials, and cultural publications. They cover overlapping themes, which makes them ideal for evaluating cross-lingual search.

---

## Document Mapping & Topics

Each document ID maps to a specific topic, linking English and Amharic concepts:

| Topic ID | Topic Title | English Document Path | Amharic Document Path |
| :--- | :--- | :--- | :--- |
| **Topic 1** | Coffee Culture & Traditions | `data/raw/english/doc1.txt` | `data/raw/amharic/doc1.txt` |
| **Topic 2** | Lalibela Rock-Hewn Churches | `data/raw/english/doc2.txt` | `data/raw/amharic/doc2.txt` |
| **Topic 3** | Addis Ababa Capital City | `data/raw/english/doc3.txt` | `data/raw/amharic/doc3.txt` |
| **Topic 4** | Lucy / Dinkenesh Fossil | `data/raw/english/doc4.txt` | `data/raw/amharic/doc4.txt` |
| **Topic 5** | Simien Mountains National Park | `data/raw/english/doc5.txt` | `data/raw/amharic/doc5.txt` |
| **Topic 6** | Ethiopian Running & Athletics | `data/raw/english/doc6.txt` | `data/raw/amharic/doc6.txt` |
| **Topic 7** | Axum Granite Obelisks | `data/raw/english/doc7.txt` | `data/raw/amharic/doc7.txt` |
| **Topic 8** | Blue Nile Falls (Tis Abay) | `data/raw/english/doc8.txt` | `data/raw/amharic/doc8.txt` |
| **Topic 9** | Ethiopian New Year (Enkutatash) | `data/raw/english/doc9.txt` | `data/raw/amharic/doc9.txt` |
| **Topic 10** | Traditional Cuisine (Injera/Wat) | `data/raw/english/doc10.txt` | `data/raw/amharic/doc10.txt` |
| **Topic 11** | Battle of Adwa (1896) | `data/raw/english/doc11.txt` | `data/raw/amharic/doc11.txt` |
| **Topic 12** | Grand Renaissance Dam (GERD) | `data/raw/english/doc12.txt` | `data/raw/amharic/doc12.txt` |

---

## Dataset Statistics

- **Format**: UTF-8 plain text files (`.txt`).
- **Average Document Length (English)**: ~65 words.
- **Average Document Length (Amharic)**: ~55 words.
- **Primary Vocabulary Size**:
  - English: ~180 unique terms (post-stemming and stopword filtering).
  - Amharic: ~160 unique terms (post-homophone normalization and stopword filtering).

## Relevance Ground Truth
The test queries in `src/evaluation/test_queries.json` map each query to relevant document IDs from this dataset. For instance, the query "coffee ceremony" maps to `["english_doc1", "amharic_doc1"]` as ground truth.
