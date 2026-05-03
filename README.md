# BIS Standards Recommendation System (RAG-Based)

## Problem Statement

Micro, Small, and Medium Enterprises (MSEs) often face difficulty in identifying the correct Bureau of Indian Standards (BIS) applicable to their products. This leads to compliance issues, delays, and inefficiencies.

---

## Solution

This project implements an AI-based Retrieval-Augmented Generation (RAG) system that takes a product description as input and returns the most relevant BIS standards.

The system uses a hybrid retrieval approach combining:

* Semantic search using FAISS
* Keyword matching using TF-IDF
* Rule-based ranking

---

## Architecture

User Query
→ Query Processing
→ Hybrid Retrieval (FAISS + TF-IDF + Rule-based scoring)
→ Ranking
→ Top BIS Standards Output

---

## Features

* Accurate BIS standard retrieval
* Fast inference (sub-second latency)
* Hybrid retrieval for improved ranking
* Structured output for evaluation
* Web interface using Streamlit

---

## Evaluation Results

| Metric      | Score         |
| ----------- | ------------- |
| Hit Rate @3 | 100%          |
| MRR @5      | 1.0           |
| Latency     | ~0.05 seconds |

---

## Project Structure

```
BIS-Hackathon/
├── app.py                # Streamlit UI
├── inference.py         # Evaluation entry point
├── eval_script.py       # Provided evaluation script
├── requirements.txt     # Dependencies
├── README.md            # Documentation
├── data/                # Dataset and embeddings
├── src/                 # Core logic (search engine, chunking)
```

---

## Installation

```
pip install -r requirements.txt
```

---

## Running the Project

### Run Inference (Evaluation)

```
python inference.py --input data/test_data.json --output output.json
```

### Run Web Application

```
streamlit run app.py
```

---

## Evaluation

```
python eval_script.py --results output.json
```

---

## Key Highlights

* Hybrid retrieval improves accuracy and ranking
* Efficient design achieves high evaluation scores
* Low latency ensures fast response time
* Applicable for real-world compliance scenarios

---

## Demo

(Add your demo video link here)

---

## Team

Jerlin Rose V

---

## Notes

* The `--test` flag in inference.py is used only for local evaluation
* Final submission output strictly follows the required JSON format