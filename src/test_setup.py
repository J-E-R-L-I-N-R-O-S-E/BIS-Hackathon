import pdfplumber
import os

print("Setup successful!")

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
pdf_path = os.path.join(project_root, "data", "dataset.pdf")

print("Looking for file at:", pdf_path)

with pdfplumber.open(pdf_path) as pdf:
    print("Total pages:", len(pdf.pages))