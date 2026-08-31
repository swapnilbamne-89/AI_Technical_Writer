# Skill: Generate Defense Document
User Input: $ARGUMENTS

## Execution Workflow
You are executing a highly structured document generation task. Follow these steps in exact order. Do not skip steps. If any step fails, halt and report the error to the user.

### Step 1: Parse Intent
Analyze the User Input to extract the following:

- Product Code (e.g., RAD-99)
- Document Title (e.g., Radar Interface)
- Document Type (e.g., QTP)
- Specific Technical Instructions provided by the user.

### Step 2: Route & Lookup Document Code
- Run the Python script: python scripts/lookup_code.py --product "<Product Code>" --type "<Document Type>"
- Extract the Document Code and Control Category from the script output.
- Guardrail Check: If the script returns "Not Found", halt and tell the user the product code does not exist in the Master List. Do not invent a code.

### Step 3: Ingest Defense Standard
- Run the Python script: python scripts/ocr_standard.py --doc_type "<Document Type>"
- This will OCR the relevant Defense Standard PDF and output the structural requirements.
-  Read the output to understand the mandatory headings, tables, and compliance rules required for this document.

### Step 4: Apply Memory & Knowledge
- Read the skills.md file to check for any past user preferences or rules.
- Read the files in the /Knowledge folder (Glossary and Style Guide).
- Guardrail Check: Ensure all terminology used in the upcoming draft strictly adheres to the Glossary.

### Step 5: Draft Content (HTML)
- Draft all content as clean, semantic HTML using standard tags (<h1>, <h2>, <p>, <table>, <ul>, <li>).
- Do NOT include inline CSS styles in the HTMLexcept for <img> tags which require width constraints.
- Ensure every mandatory heading and table required by the Defense Standard (from OCR) is present in the HTML. If data is missing, insert "[REQUIRES USER INPUT]".
- PROTOCOL DATA RULE: If the user provides Binary or NMEA protocol data, insert it exactly as provided. Wrap it in an HTML <pre> tag to preserve formatting, and add a visible warning flag directly above it: <p class="note">[MANUAL VERIFICATION REQUIRED: BINARY/NMEA PROTOCOL DATA]</p>.
- ASSET AUTO-RECOGNITION RULE:
1. Extract the Product Family and Series from the user's input (e.g., Product Code "OCT3-T-99" -> Family: OCT3, Series: T).
2. List the files in the /assets folder.
3. Look for files starting with that Product Family and Series (e.g., OCT3_T+*.png).
4. If a matching file is found, read it, convert to Base64, and embed it using the <figure> tag.
5. Parse the filename according to the Image Naming Convention Protocol in CLAUDE.md to auto-generate the correct <figcaption>.
6. If no matching image is found, insert the [REQUIRES USER INPUT] placeholder.

### Step 6: Generate MS Word Document
- Run the Python script: python scripts/generate_doc.py --html_output "<drafted_html>" --docx_name "<Document Code>_<Document Title>.docx" --doc_type "<Document Type>"
- The script will merge the HTML, the General CSS, and the MS Word Template, saving the final .docx in /Output/.

### Step 7: Critique & Validate
- Run the Python script: python scripts/critique_doc.py --docx_path "/Output/<Document Code>_<Document Title>.docx"
- Review the critic's output. If there are formatting errors, missing standards, or style guide violations, fix them in the HTML and re-run Step 6.

### Step 8: Save Draft & Report
- Save the final HTML string used in Step 6 to the /drafts folder as <Document Code>_<Document Title>.html.
- Confirm to the user that the document has been generated, the draft saved, and summarize any critiques.
- SYNC WARNING: Remind the user: "If you make manual edits to this Word document, please notify me before requesting any future updates so I can sync the HTML draft and prevent data loss."

### Step 8: Save Draft & Report
- Save the final HTML string used in Step 6 to the /drafts folder as <Document Code>_<Document Title>.html.
- Confirm to the user that the document has been generated, the draft saved, and summarize any critiques.
- SYNC WARNING: Remind the user: "If you make manual edits to this Word document, please notify me before requesting any future updates so I can sync the HTML draft and prevent data loss."
- TOC REMINDER: Remind the user: "The Table of Contents and List of Figures have been inserted as placeholders. Please open the document in MS Word, select all (Ctrl+A), and press F9 (or right-click the ToC and select 'Update Field') to populate the page numbers."