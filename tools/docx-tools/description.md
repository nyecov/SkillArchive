# DOCX Tools

A Python automation script using `python-docx` to read and generate Word documents programmatically.

**Primary Uses:**
1. Extracting text paragraphs and tables from an existing `.docx` into structured JSON for LLM context injection.
2. Generating a fresh `.docx` file from text strings (e.g., saving a generated report or summary).

**Usage:**
```bash
# Extract
python docx_tools.py extract path/to/document.docx

# Create
python docx_tools.py create path/to/output.docx --title "Report" --text "Paragraph 1" "Paragraph 2"
```
