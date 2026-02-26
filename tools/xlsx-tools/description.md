# XLSX Tools

A Python script using `openpyxl` to extract data from Excel spreadsheets efficiently.

**Primary Uses:**
1. Reading `.xlsx` files without needing Excel installed.
2. Extracting all sheets (or a specific sheet) into a structured JSON dictionary of arrays.
3. Automatically filtering out completely empty rows to save tokens when passing the data to an LLM.

**Usage:**
```bash
# Extract all sheets
python xlsx_tools.py path/to/spreadsheet.xlsx

# Extract a specific sheet
python xlsx_tools.py path/to/spreadsheet.xlsx --sheet "Q3 Financials"
```
