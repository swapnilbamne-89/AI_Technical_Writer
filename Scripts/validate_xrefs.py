import argparse
import os
import re

def validate_cross_references(html_file_path):
    if not os.path.exists(html_file_path):
        print("STATUS: ERROR")
        print(f"ERROR: HTML draft not found at {html_file_path}")
        return

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 1. Find all IDs in the HTML (e.g., <table id="tab-1">, <figure id="fig-1">)
        # Matches id="anything" or id='anything'
        id_pattern = r'id=["\'](.*?)["\']'
        existing_ids = set(re.findall(id_pattern, html_content))

        # 2. Find all cross-reference links (e.g., <a href="#tab-1">Table 1</a>)
        # Matches href="#anything"
        href_pattern = r'href=["\']#(.*?)["\']'
        referenced_ids = set(re.findall(href_pattern, html_content))

        # 3. Compare to find broken links
        broken_links = []
        for ref_id in referenced_ids:
            if ref_id not in existing_ids:
                broken_links.append(ref_id)

        # --- OUTPUT RESULTS ---
        print("STATUS: SUCCESS")
        if not broken_links:
            print("XREF VALIDATION: PASS - All cross-references point to valid targets.")
        else:
            print("XREF VALIDATION: FAIL - Broken cross-references found:")
            for broken in broken_links:
                print(f"- Missing target: #{broken}")

    except Exception as e:
        print("STATUS: ERROR")
        print(f"ERROR: Failed to validate cross-references. {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--html_path", required=True, help="Path to the HTML draft file")
    args = parser.parse_args()
    
    validate_cross_references(args.html_path)