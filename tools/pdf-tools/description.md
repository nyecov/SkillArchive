# PDF Tools

A Python tool leveraging `PyMuPDF` (`fitz`) for fast, robust PDF manipulation.

**Primary Uses:**
1. Extracting raw text from a PDF document for analysis.
2. Extracting text as structured JSON containing metadata (page numbers, image counts per page).
3. Merging multiple PDFs sequentially into a single file.

**Usage:**
```bash
# Extract raw text
python pdf_tools.py extract path/to/file.pdf

# Extract as JSON
python pdf_tools.py extract path/to/file.pdf --json

# Merge
python pdf_tools.py merge file1.pdf file2.pdf -o merged.pdf
```
