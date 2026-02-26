import sys
import argparse
import json
try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) is required. Install with: pip install PyMuPDF")
    sys.exit(1)

def extract_text(pdf_path, output_json=False):
    """Extracts text from a PDF, optionally returning JSON with page metadata."""
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        sys.exit(1)

    pages_data = []
    full_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        full_text.append(text)
        
        if output_json:
            pages_data.append({
                "page": page_num + 1,
                "text": text.strip(),
                "images_count": len(page.get_images())
            })

    doc.close()

    if output_json:
        print(json.dumps({"total_pages": len(pages_data), "pages": pages_data}, indent=2))
    else:
        print("\n--- PAGE ".join([""] + full_text))


def merge_pdfs(pdf_list, output_path):
    """Merges multiple PDFs into one."""
    result = fitz.open()
    for pdf in pdf_list:
        try:
            with fitz.open(pdf) as doc:
                result.insert_pdf(doc)
        except Exception as e:
            print(f"Warning: skipped {pdf} due to error: {e}")
            
    result.save(output_path)
    result.close()
    print(f"Merged {len(pdf_list)} documents into {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Manipulation Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract text from PDF")
    extract_parser.add_argument("file", help="Path to PDF file")
    extract_parser.add_argument("--json", action="store_true", help="Output as JSON with metadata")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDFs")
    merge_parser.add_argument("files", nargs="+", help="Paths to PDF files to merge")
    merge_parser.add_argument("-o", "--output", required=True, help="Output merged PDF path")

    args = parser.parse_args()

    if args.command == "extract":
        extract_text(args.file, args.json)
    elif args.command == "merge":
        merge_pdfs(args.files, args.output)
