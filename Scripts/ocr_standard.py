"""
Extracts text from a standards PDF in /Standards. Tries direct text
extraction first (fast, exact, works for any digital-native PDF); falls
back to OCR only if that comes back suspiciously empty, which usually
means the PDF is a scan.

Requires locally: poppler (for pdf2image) and tesseract (for pytesseract)
if the OCR fallback path is ever needed. Native extraction alone covers
most modern standards PDFs.
"""
import sys
from pathlib import Path


def extract_text(pdf_path: str) -> str:
    pdf_path = Path(pdf_path)
    text = _extract_native(pdf_path)
    if len(text.strip()) < 200:  # too little text -> probably a scanned PDF
        text = _extract_ocr(pdf_path)
    return text


def _extract_native(pdf_path: Path) -> str:
    import pdfplumber
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            chunks.append(page.extract_text() or "")
    return "\n".join(chunks)


def _extract_ocr(pdf_path: Path) -> str:
    from pdf2image import convert_from_path
    import pytesseract
    pages = convert_from_path(str(pdf_path))
    return "\n".join(pytesseract.image_to_string(p) for p in pages)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ocr_standard.py <path_to_pdf>")
        sys.exit(1)
    print(extract_text(sys.argv[1]))
