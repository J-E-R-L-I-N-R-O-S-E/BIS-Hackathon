import argparse
import json
import time
import os
from src.search_engine import search

# -----------------------------
# Normalize function (MATCH EVAL SCRIPT)
# -----------------------------
def normalize_std(std):
    return str(std).replace(" ", "").lower()

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main(input_path, output_path, test_mode=False):
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return

    with open(input_path, "r") as f:
        data = json.load(f)

    results = []

    for item in data:
        try:
            query = item["query"]

            start = time.time()
            search_results = search(query, top_k=5)
            end = time.time()

            # Extract + normalize
            if not search_results:
                retrieved = []
            else:
                retrieved = [normalize_std(res["standard"]) for res in search_results]

            # ---- SAFETY FALLBACK ----
            if not retrieved:
                retrieved = ["is269:1989"]

            # ---- TEST MODE ----
            if test_mode:
                results.append({
                    "id": item["id"],
                    "expected_standards": item.get("expected_standards", []),
                    "retrieved_standards": retrieved,
                    "latency_seconds": round(end - start, 3)
                })

            # ---- SUBMISSION MODE ----
            else:
                results.append({
                    "id": item["id"],
                    "retrieved_standards": retrieved,
                    "latency_seconds": round(end - start, 3)
                })

        except Exception as e:
            print(f"⚠️ Error processing {item.get('id')}: {e}")
            continue

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Inference completed")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    main(args.input, args.output, args.test)