import pdfplumber
import os
import re
import json


# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# -----------------------------
# Clean text
# -----------------------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Page \d+", "", text)
    return text


# -----------------------------
# Detect category (VERY IMPORTANT)
# -----------------------------
def detect_category(content):
    content = content.lower()

    if "cement" in content:
        return "Cement"
    elif "aggregate" in content or "aggregates" in content:
        return "Aggregates"
    elif "concrete" in content:
        return "Concrete"
    elif "steel" in content:
        return "Steel"
    else:
        return "General"


# -----------------------------
# Split into BIS standards
# -----------------------------
def split_into_standards(text):
    # Match patterns like IS 269: 1989 OR IS 2185 (Part 2): 1983
    chunks = re.split(r"(IS\s\d+(\s\(Part\s\d+\))?[:\-]\s?\d{4})", text)

    standards = []

    for i in range(1, len(chunks), 3):
        standard_id = chunks[i].strip()
        content = chunks[i + 2].strip()

        if len(content) < 100:
            continue

        standards.append({
            "standard": standard_id,
            "category": detect_category(content),
            "content": content
        })

    return standards


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("🚀 Phase 1: Chunking started...")

    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    pdf_path = os.path.join(project_root, "data", "dataset.pdf")

    print("📄 Extracting text...")
    text = extract_text(pdf_path)

    print("🧹 Cleaning text...")
    text = clean_text(text)

    print("✂️ Splitting into standards...")
    standards = split_into_standards(text)

    print(f"✅ Total standards found: {len(standards)}")

    output_path = os.path.join(project_root, "data", "standards.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(standards, f, indent=2)

    print("💾 Saved to:", output_path)