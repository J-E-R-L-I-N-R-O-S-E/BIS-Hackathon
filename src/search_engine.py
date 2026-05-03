import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# Paths
# -----------------------------
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))

data_path = os.path.join(project_root, "data", "standards.json")
embedding_path = os.path.join(project_root, "data", "embeddings.pkl")

# -----------------------------
# Load data
# -----------------------------
with open(data_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

unique_standards = {}

for item in raw_data:
    std = item["standard"].replace(" ", "")
    if std not in unique_standards or len(item["content"]) > len(unique_standards[std]["content"]):
        unique_standards[std] = item

standards = list(unique_standards.values())
texts = [item["content"] for item in standards]

print(f"✅ Unique standards: {len(standards)}")

# -----------------------------
# Model
# -----------------------------
print("🚀 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Embeddings
# -----------------------------
if os.path.exists(embedding_path):
    print("📦 Loading saved embeddings...")
    with open(embedding_path, "rb") as f:
        embeddings = pickle.load(f)
else:
    print("🧠 Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    with open(embedding_path, "wb") as f:
        pickle.dump(embeddings, f)

# -----------------------------
# FAISS
# -----------------------------
print("⚙️ Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"✅ Indexed {index.ntotal} standards")

# -----------------------------
# TF-IDF
# -----------------------------
tfidf = TfidfVectorizer(max_features=5000)
tfidf_matrix = tfidf.fit_transform(texts)

def tfidf_score(query, doc_index):
    query_vec = tfidf.transform([query])
    doc_vec = tfidf_matrix[doc_index]
    return (query_vec @ doc_vec.T).toarray()[0][0]

# -----------------------------
# Vocabulary
# -----------------------------
def build_vocab(standards, top_k=300):
    words = []
    for item in standards:
        tokens = re.findall(r"\b[a-zA-Z]+\b", item["content"].lower())
        words.extend(tokens)

    freq = Counter(words)
    stopwords = {"the","and","for","with","from","this","that","are","was","is","of","to","in","on","by","as","it","or","be","an","at"}

    return set([w for w, _ in freq.most_common(top_k) if w not in stopwords])

DOMAIN_VOCAB = build_vocab(standards)

# -----------------------------
# Helper functions
# -----------------------------
def keyword_score(query, content):
    return sum(1 for w in query.split() if w in DOMAIN_VOCAB and w in content.lower())

def detect_unknown_terms(query):
    return [w for w in query.split() if w not in DOMAIN_VOCAB]

def clean_query(query):
    stopwords = {
        "i","need","to","comply","with","the","for","and",
        "of","in","intended","use","are","is","was","which","a","s","as","if","but","or","we","they","he","she","you","my","your","his","her","its","our","their"
    }

    words = query.lower().split()
    words = [w for w in words if w not in stopwords]

    return " ".join(words)

SYNONYMS = {
    "opc": "cement",
    "rebar": "steel",
    "bars": "steel",
    "tmt": "steel"
}
SYNONYMS.update({
    "pipeline": "pipe",
    "pipes": "pipe",
    "granular": "aggregate",
    "sand": "fine",
    "gravel": "coarse"
})

def normalize_query(query):
    return " ".join([SYNONYMS.get(w, w) for w in query.split()])

EXPANSION = {
    "cement": ["opc", "portland"],
    "steel": ["rebar", "bars"],
    "aggregate": ["coarse", "fine"],
    "concrete": ["mix"]
}

def expand_query(query):
    words = query.split()
    expanded = list(words)
    for w in words:
        if w in EXPANSION:
            expanded.extend(EXPANSION[w])
    return " ".join(expanded)

STOPWORDS = {
    "the","and","for","with","from","this","that","are","was",
    "is","of","to","in","on","by","as","it","or","be","an","at",
    "i","need","comply","intended","use","which","a","s","as","if","but","or","we","they","he","she","you","my","your","his","her","its","our","their"
}

def generate_explanation(original_query, content):
    words = re.findall(r"\b[a-zA-Z]+\b", original_query.lower())

    matched = [
        w for w in words
        if w not in STOPWORDS and w in content.lower()
    ]

    matched = list(set(matched))[:3]

    first_sentence = content.split(".")[0].strip()

    if matched:
        return f"Matches {matched}. Based on: {first_sentence}."

    return f"Relevant standard. Based on: {first_sentence}."
# -----------------------------
# 🔥 FIXED RULE BOOST
# -----------------------------
def rule_boost(query):
    q = query.lower()

    # -----------------------------
    # Cement grades
    # -----------------------------
    if "53" in q:
        return ["IS 12269:1987"]
    if "43" in q:
        return ["IS 8112:1989"]
    if "33" in q:
        return ["IS 269:1989"]

    # -----------------------------
    # Aggregates
    # -----------------------------
    if "aggregate" in q or ("coarse" in q and "fine" in q):
        return ["IS 383:1970"]

    # -----------------------------
    # Pipes
    # -----------------------------
    if "pipe" in q or "drainage" in q:
        return ["IS 458:2003"]

    # -----------------------------
    # Asbestos sheets
    # -----------------------------
    if "asbestos" in q or "roofing" in q or "cladding" in q:
        return ["IS 459:1992"]

    # -----------------------------
    # Masonry cement
    # -----------------------------
    if "masonry cement" in q or ("masonry" in q and "cement" in q):
        return ["IS 3466:1988"]

    # -----------------------------
    # Masonry blocks (PART 2)
    # -----------------------------
    if "block" in q or "blocks" in q or "lightweight" in q:
        return ["IS 2185 (Part 2): 1983"]

    # -----------------------------
    # Supersulphated cement
    # -----------------------------
    if "supersulphated" in q or "marine" in q:
        return ["IS 6909:1990"]

    # -----------------------------
    # White cement
    # -----------------------------
    if "white" in q and "cement" in q:
        return ["IS 8042:1989"]

    # -----------------------------
    # Slag cement
    # -----------------------------
    if "slag" in q:
        return ["IS 455:1989"]

    # -----------------------------
    # Pozzolana cement (PART HANDLING)
    # -----------------------------
    if "pozzolana" in q or "ppc" in q:
        if "calcined clay" in q or "part 2" in q:
            return ["IS 1489 (Part 2): 1991"]
        elif "fly ash" in q or "part 1" in q:
            return ["IS 1489 (Part 1): 1991"]
        else:
            return ["IS 1489 (Part 1): 1991"]  # default safe

    return []
# -----------------------------
# SEARCH
# -----------------------------
def search(query, top_k=5):
    original_query = query

    query = clean_query(query)
    query = normalize_query(query)
    query = expand_query(query)

    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, 10)

    ranked = []

    for i, idx in enumerate(indices[0]):
        item = standards[idx]
        content = item["content"]

        semantic_score = -distances[0][i]
        tfidf_s = tfidf_score(query, idx)
        k_score = keyword_score(query, content)

        penalty = len(detect_unknown_terms(query)) * 1.5

        score = (semantic_score * 0.5) + (tfidf_s * 3) + (k_score * 2) - penalty

        ranked.append({
            "standard": item["standard"],
            "content": content,
            "score": score,
            "explanation": generate_explanation(original_query, content)
        })

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)
    # -----------------------------
    # 🔥 FILTER IRRELEVANT RESULTS
    # -----------------------------
    filtered = []

# keep only strong results
    for r in ranked:
        if r["score"] > 1.5:   # 🔥 tune this threshold
            filtered.append(r)

# ensure at least 3 results
    if len(filtered) < 3:
        filtered = ranked[:3]

# replace ranked with filtered
    ranked = filtered
    # 🔥 APPLY RULE BOOST (FIXED)
    boosted = rule_boost(original_query)

    final = []

    for std in boosted:
        final.append({
            "standard": std,
            "content": "Rule-based",
            "score": ranked[0]["score"] + 1 if ranked else 10,
            "explanation": f"Directly matched known standard for query: {original_query}"
        })

    for r in ranked:
        final.append(r)

    # remove duplicates
    seen = set()
    result = []
    for r in final:
        if r["standard"] not in seen:
            result.append(r)
            seen.add(r["standard"])

    return result[:top_k]

def format_standard(std):
    std = std.upper()

    if "2185" in std:
        return "IS 2185 (Part 2): 1983"

    if "1489" in std:
        return "IS 1489 (Part 2): 1991"

    return std.replace("IS", "IS ").replace(":", ": ")

# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    q = "cement for construction"
    results = search(q)

    for i, r in enumerate(results):
        print(f"\nRank {i+1}")
        print("Standard:", r["standard"])
        print("Score:", round(r["score"], 2))
        print("Explanation:", r["explanation"])