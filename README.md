# BIS Standards Recommendation System (RAG-Based)

## Problem Statement

Micro, Small, and Medium Enterprises (MSEs) often face difficulty in identifying the correct Bureau of Indian Standards (BIS) applicable to their products. This leads to compliance issues, delays, and inefficiencies.

---

## Solution

This project implements a Retrieval-Augmented Generation (RAG)-based system that takes a product description as input and returns the most relevant BIS standards.

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
* Interactive web interface using Streamlit

---

## Evaluation Results

| Metric      | Score     |
| ----------- | --------- |
| Hit Rate @3 | 100%      |
| MRR @5      | 1.0       |
| Latency     | ~0.05 sec |

---

## Project Structure

```
BIS-Hackathon/
├── app.py                # Streamlit UI
├── inference.py          # Evaluation entry point
├── eval_script.py        # Provided evaluation script
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── data/                 # Dataset and embeddings
│   ├── test_data.json
│   ├── embeddings.pkl
├── src/                  # Core logic
│   ├── search_engine.py
│   ├── api.py
```

---

## 🛠️ Complete Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/J-E-R-L-I-N-R-O-S-E/BIS-Hackathon.git
cd BIS-Hackathon
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Ensure embeddings file exists

```
data/embeddings.pkl
```

---

## ▶️ Running Backend Server

```
python src/api.py
```

---

## 🌐 Run Web Application

```
streamlit run app.py
```

---

## 🧪 Run Inference (Evaluation)

```
python inference.py --input data/test_data.json --output output.json --test
python eval_script.py --results output.json
```

---

## 🏁 Final Submission Command (Used by Judges)

```
python inference.py --input hidden_private_dataset.json --output team_results.json
```

---

## 📊 Evaluation Metrics

* Hit Rate @3
* Mean Reciprocal Rank (MRR @5)
* Average Latency

---

## 💡 Methodology

1. Convert user query into embeddings
2. Perform hybrid retrieval (FAISS + TF-IDF)
3. Apply rule-based ranking
4. Return top BIS standards with explanations

---

## ⚠️ Important Note

The system depends on pre-generated embeddings.

Ensure the following file is present before running inference:

```
data/embeddings.pkl
```

If this file is missing, the system will not function correctly.

---

## 🔑 Key Highlights

* Hybrid retrieval improves ranking accuracy
* High evaluation scores achieved
* Low latency ensures fast responses
* Applicable to real-world compliance scenarios

---

## 🎥 Demo

(Add your demo video link here)

---

## 👤 Team

Jerlin Rose V
Team: Peekaboo

---

## 📌 Notes

* The `--test` flag is used only for local evaluation
* Final submission output strictly follows the required JSON format
* Ensure all dependencies are installed before running

---

## 📢 Disclaimer

This system is designed to assist in BIS standard discovery and should be used alongside official BIS documentation.
