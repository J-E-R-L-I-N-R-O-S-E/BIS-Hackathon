from fastapi import FastAPI
from pydantic import BaseModel
from src.search_engine import search

app = FastAPI(title="BIS Recommendation API")


# -----------------------------
# Request Schema
# -----------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------
# Query Validation
# -----------------------------
def is_valid_query(query):
    q = query.lower().strip()

    keywords = [
        "cement", "opc", "grade",
        "steel", "reinforcement", "rebar", "bar",
        "aggregate", "concrete", "pipe", "drainage"
    ]

    if any(word in q for word in keywords):
        return True

    if len(q) < 3:
        return False

    return False


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/search")
def search_api(request: QueryRequest):
    query = request.query

    # -----------------------------
    # VALIDATION CHECK
    # -----------------------------
    if not is_valid_query(query):
        return {
            "query": query,
            "standards": [],
            "confidence": 0,
            "message": "⚠️ Please enter a meaningful construction-related query"
        }

    # -----------------------------
    # SEARCH
    # -----------------------------
    results = search(query, top_k=5)

    # -----------------------------
    # FORMAT OUTPUT
    # -----------------------------
    standards = [
        {
            "standard": r["standard"],
            "explanation": r.get("explanation", "")
        }
        for r in results
    ]

    # -----------------------------
    # CONFIDENCE CALCULATION
    # -----------------------------
    top_score = float(results[0]["score"]) if results else 0.0
    second_score = float(results[1]["score"]) if len(results) > 1 else 0.0

    gap = top_score - second_score

    confidence = round(
        min(1.0, max(0.3, (top_score / 6) + (gap / 4))),
        2
    )
    if "Directly matched" in standards[0]["explanation"]:
        confidence = 0.9

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    response = {
        "query": query,
        "standards": standards,
        "confidence": confidence,
    }

    # -----------------------------
    # LOW CONFIDENCE WARNING
    # -----------------------------
    if confidence < 0.4:
        response["message"] = "⚠️ Low confidence. Results may be less relevant."

    return response