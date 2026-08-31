import argparse
import os
from docx import Document
import re

def critique_document(docx_path, standard_headings):
    if not os.path.exists(docx_path):
        print("STATUS: ERROR")
        print(f"ERROR: Document not found at {docx_path}")
        return

    try:
        doc = Document(docx_path)
        full_text = []
        doc_headings = []

        # Extract text and headings from the Word doc
        for para in doc.paragraphs:
            full_text.append(para.text)
            if para.style.name.startswith('Heading'):
                doc_headings.append(para.text.strip().lower())

        text_block = "\n".join(full_text).lower()
        
        # --- VALIDATION CHECKS ---
        
        issues_found = []

        # 1. Forbidden Words Check (ITAR/EAR / Style Guide)
        forbidden_words = ["unencrypted", "classified", "proprietary", "black box"] # Add your banned words here
        for word in forbidden_words:
            if word in text_block:
                issues_found.append(f"SECURITY ALERT: Forbidden word '{word}' found in document.")

        # 2. Passive Voice Check (Simple heuristic)
        # Looks for "was", "were", "been" followed by a verb ending in "ed"
        passive_matches = re.findall(r'\b(was|were|been|is|are)\b\s+\b\w+ed\b', text_block)
        if len(passive_matches) > 3: # Allow a tolerance of 3
            issues_found.append(f"STYLE GUIDE ALERT: Found {len(passive_matches)} instances of passive voice. Rewrite in active voice.")

        # 3. Missing Standard Headings Check
        # standard_headings is passed as a comma-separated string
        expected_headings = [h.strip().lower() for h in standard_headings.split(',')]
        missing_headings = []
        for heading in expected_headings:
            if heading and heading not in doc_headings:
                missing_headings.append(heading)
        
        if missing_headings:
            issues_found.append(f"STANDARDS ALERT: Missing mandatory headings: {', '.join(missing_headings)}")

        # --- OUTPUT RESULTS ---
        print("STATUS: SUCCESS")
        if not issues_found:
            print("CRITIQUE: PASS - Document meets all compliance, style, and formatting rules.")
        else:
            print("CRITIQUE: FAIL - Issues found that require human or AI correction:")
            for issue in issues_found:
                print(f"- {issue}")

    except Exception as e:
        print("STATUS: ERROR")
        print(f"ERROR: Failed to critique document. {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docx_path", required=True, help="Path to the generated .docx file")
    parser.add_argument("--standard_headings", required=True, help="Comma-separated list of mandatory headings from the Defense Standard")
    args = parser.parse_args()
    
    critique_document(args.docx_path, args.standard_headings)