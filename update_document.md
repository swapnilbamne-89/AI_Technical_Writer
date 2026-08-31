# Skill: Update Existing Defense Document
User Input: $ARGUMENTS

## Execution Workflow
You are updating an existing document based on new user inputs. Follow these steps strictly.

## Step 1: Parse Update Intent
Analyze the User Input to identify:

1. The name/Document Code of the existing document to be updated.
2. The specific changes or new technical inputs the user wants to apply.
## Step 2: Load the HTML Draft
- Locate the corresponding HTML file in the /drafts folder (e.g., /drafts/DEF-RAD-99-001_Radar_Interface.html).
- Read the contents of this HTML file.
- Guardrail Check: If the HTML draft does not exist, halt and tell the user: "Draft not found. Cannot update document. Please generate the document first."
## Step 3: Apply Knowledge & Updates
- Read the /Knowledge folder (Glossary and Style Guide).
- Apply the user's requested changes directly to the HTML code.
- Ensure any new terminology adheres to the Glossary Lock rule.
## Step 4: Regenerate MS Word Document
- Run the Python script: python scripts/generate_doc.py --html_output "<updated_html>" --docx_name "<Original Document Name>.docx" --doc_type "<Document Type>"
- This will overwrite the old file in the /Output folder with the updated version.
## Step 5: Report Changes
- Confirm to the user that the document has been updated.
- Provide a clear, bulleted summary of exactly what was changed in the document (e.g., "Updated temperature range from -40C to -50C in Section 3.2").
- Update the /drafts HTML file with the new content.