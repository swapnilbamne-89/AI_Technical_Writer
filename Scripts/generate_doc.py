import argparse
import os
from htmldocx import HtmlToDocx
from docx import Document

def convert_html_to_docx(html_content, docx_name, doc_type):
    # Define paths
    styles_dir = os.path.join('..', 'styles')
    templates_dir = os.path.join('..', 'Templates')
    output_dir = os.path.join('..', 'output')
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Load the General CSS
    css_file = os.path.join(styles_dir, 'general_style.css')
    css_content = ""
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
    else:
        print(f"WARNING: General CSS file not found at {css_file}.")

    # 2. Combine CSS and HTML
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
        {css_content}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # 3. Find and Open the Specific MS Word Template
    template_file = os.path.join(templates_dir, f'{doc_type.upper()}_Template.docx')
    
    if os.path.exists(template_file):
        # Open the existing template (preserves logos, footers, margins)
        docx = Document(template_file)
        print(f"STATUS: INFO - Loaded template: {template_file}")
    else:
        # Fallback to a blank document if template isn't found
        print(f"WARNING: Template not found at {template_file}. Creating blank document.")
        docx = Document()

    # 4. Convert HTML/CSS and append to the Template
    try:
        parser = HtmlToDocx()
        # The parse_html_string method can accept an existing document object
        docx = parser.parse_html_string(full_html, docx=docx)
        
        # Save the final document
        docx_path = os.path.join(output_dir, docx_name)
        docx.save(docx_path)
        
        print("STATUS: SUCCESS")
        print(f"MESSAGE: Document successfully generated at {docx_path}")
        
    except Exception as e:
        print("STATUS: ERROR")
        print(f"ERROR: Failed to generate document. {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--html_output", required=True, help="The drafted HTML content")
    parser.add_argument("--docx_name", required=True, help="The name of the output .docx file")
    parser.add_argument("--doc_type", required=True, help="The document type (e.g., QTP)")
    args = parser.parse_args()
    
    convert_html_to_docx(args.html_output, args.docx_name, args.doc_type)