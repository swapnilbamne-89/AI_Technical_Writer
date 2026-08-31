# Skill: Update Existing Defense Document
User Input: $ARGUMENTS

## Execution Workflow
You are updating an existing document based on new user inputs. Follow these steps strictly.

### Step 1: Parse Update Intent
Analyze the User Input to identify:
1. The name or Document Code of the existing document to be updated.
2. The specific changes or new technical inputs the user wants to apply.

### Step 2: Sync Check & Human Edit Detection
- Locate the corresponding HTML file in the /drafts folder (e.g., /drafts/DEF-RAD-99-001_Radar_Interface.html).
- GUARDRAIL CHECK: Before reading the HTML, you MUST ask the user: "Have you made any manual edits to the Word document since it was last generated? (Yes/No)"
- If the user says "Yes" or "Unsure":
	1. HALT the update process. Do not modify the HTML yet.
	2. Tell the user: "To prevent overwriting your manual edits, please either:A) Copy and paste the manually edited text from Word into this chat so I can update the HTML draft, ORB) Confirm that you want me to overwrite the Word document based on the old AI draft (this will erase your manual edits)."
	3. Wait for the user's response. If they provide text, update the HTML draft first. If they confirm overwrite, proceed.
- If the user says "No":
	1. Proceed to Step 3.
- GUARDRAIL CHECK: If the HTML draft does not exist at all, halt and tell the user: "Draft not found. Cannot update document. Please generate the document first using /generate_document."

### Step 3:  Sync Check & Human Edit Detection
- Read the files in the /Knowledge folder (Glossary and Style Guide).
- Apply the user's requested changes directly to the HTML code.
- Ensure any new terminology adheres to the Glossary Lock rule.
- Cross-Reference Check: If tables/figures were added or deleted, follow the Renumbering Rule in CLAUDE.md to update all IDs and anchor links.
- PROTOCOL DATA BLOCK: If the user's requested changes involve modifying Binary data, Hex strings, or NMEA sentences, you MUST halt the update for that specific section. Do not change the HTML. Inform the user: "I cannot modify Binary or NMEA protocol data. You must manually update this section in the final Word document."
- HIGHLIGHTING RULE: You MUST wrap ALL modified or newly added text in <span class="ai-update">...</span> so it appears yellow in the final Word document.

### Step 4: Validate Cross-References
- Run the Python script: python scripts/validate_xrefs.py --html_path "/drafts/<Document Name>.html"
- Read the output. If the script returns "FAIL", halt and fix the broken HTML anchors before proceeding.

### Step 5: Regenerate MS Word Document
- Run the Python script: python scripts/generate_doc.py --html_output "<updated_html>" --docx_name "<Original Document Name>.docx" --doc_type "<Document Type>"
- This will overwrite the old file in the /Output folder with the updated version.

### Step 6: Report Changes & Update Memory
- Confirm to the user that the document has been successfully updated.
- Provide a clear, bulleted summary of exactly what was changed in the document (e.g., "Deleted Table 2, renumbered Table 3 to Table 2, updated 2 cross-references").
- Save the updated HTML string back to the /drafts folder, overwriting the old draft. Ensure the <span class="ai-update"> tags are REMOVED from the saved draft so they don't persist into the next update cycle.
- Memory Check: If the user's update represents a general rule, append this rule to the skills.md file.