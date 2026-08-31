# Skill: Critique & Validate Defense Document
User Input: $ARGUMENTS

## Execution Workflow
You are acting as a strict Quality Assurance Critic for defense documentation. Follow these steps.

### Step 1: Parse Intent
Analyze the User Input to identify:

1. The name of the document to critique (e.g., DEF-RAD-99-001_Radar_Interface.docx).
2. The Document Type (e.g., QTP) to know which standard to check against.
### Step 2: Extract Mandatory Headings
- Run python scripts/ocr_standard.py --doc_type "<Document Type>"
- Parse the output to identify the mandatory top-level headings required by the defense standard.
- Convert this list into a comma-separated string.
### Step 3: Run Programmatic Critique
- Run the Python script: python scripts/critique_doc.py --docx_path "/Output/<Document Name>.docx" --standard_headings "<comma_separated_headings>"
- Read the output of the script carefully.
### Step 4: AI Semantic Critique
In addition to the script's programmatic checks, read the HTML draft from the /drafts folder and perform a semantic review:

1. Glossary Check: Are there any terms used that are not in the approved Glossary?
2. Context Check: Does the technical data make sense based on the user's original inputs?
3. Formatting: Are there any broken HTML tags or missing tables?
### Step 5: Report to User
Provide a comprehensive Critique Report to the user in this format:

- Programmatic Validation: [PASS/FAIL] (Summarize any security alerts, passive voice, or missing headings found by the script).
- Semantic Validation: [PASS/FAIL] (Summarize any glossary, context, or formatting issues you noticed).
- Recommended Actions: Provide a bulleted list of exact steps needed to fix the document.
- Ask the user if they would like you to automatically apply these fixes.