#!/usr/bin/env python3
"""
Script to update docs.json navigation to use custom labels from MDX file titles.
This prevents Mintlify from prefixing page titles with the group name.
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional

def extract_frontmatter_title(file_path: Path) -> Optional[str]:
    """Extract the title from an MDX file's frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return None
        
        frontmatter = frontmatter_match.group(1)
        title_match = re.search(r'^title:\s*[\'"](.*?)[\'"]', frontmatter, re.MULTILINE)
        if title_match:
            return title_match.group(1)
        return None
    except Exception:
        return None


def convert_page_to_object(page_path: str, base_dir: Path) -> Dict:
    """Convert a page path string to an object with page and label."""
    # Convert path to file path
    file_path = base_dir / f"{page_path}.mdx"
    
    # Try to get title from MDX file
    title = extract_frontmatter_title(file_path)
    
    if title:
        return {"page": page_path, "label": title}
    else:
        # Fallback: use the path as-is (shouldn't happen, but just in case)
        return page_path


def update_navigation_with_labels(docs_json_path: Path, base_dir: Path):
    """Update docs.json to use custom labels for all pages."""
    # Read the current docs.json
    with open(docs_json_path, 'r', encoding='utf-8') as f:
        docs = json.load(f)
    
    # Process each tab
    for tab in docs.get("navigation", {}).get("tabs", []):
        # Process each group
        for group in tab.get("groups", []):
            pages = group.get("pages", [])
            updated_pages = []
            
            for page in pages:
                if isinstance(page, str):
                    # Convert string path to object with label
                    page_obj = convert_page_to_object(page, base_dir)
                    updated_pages.append(page_obj)
                elif isinstance(page, dict):
                    # Already an object, but update label if needed
                    page_path = page.get("page", page.get("path", ""))
                    if page_path:
                        file_path = base_dir / f"{page_path}.mdx"
                        title = extract_frontmatter_title(file_path)
                        if title:
                            page["label"] = title
                    updated_pages.append(page)
                else:
                    # Keep as-is (shouldn't happen)
                    updated_pages.append(page)
            
            group["pages"] = updated_pages
    
    # Write back to docs.json
    with open(docs_json_path, 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Updated {docs_json_path} with custom labels for all pages")


def main():
    """Main function."""
    base_dir = Path(__file__).parent
    docs_json_path = base_dir / "docs.json"
    
    if not docs_json_path.exists():
        print(f"✗ Error: {docs_json_path} not found")
        return
    
    print("Updating docs.json navigation with custom labels...\n")
    update_navigation_with_labels(docs_json_path, base_dir)
    print("\nDone!")


if __name__ == "__main__":
    main()

