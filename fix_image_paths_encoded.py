#!/usr/bin/env python3
"""
Fix image paths in MDX files by URL-encoding spaces in HTML img src attributes.
"""

import os
import re
from pathlib import Path
from urllib.parse import quote

def fix_image_paths_in_file(file_path):
    """Fix image paths in a single MDX file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find HTML img tags with paths containing spaces
    pattern = r'<img src="(/images/[^"]+)" alt="" />'
    
    def encode_spaces(match):
        path = match.group(1)
        # URL-encode the path properly - encode spaces and special chars but keep slashes
        parts = path.split('/')
        encoded_parts = [parts[0]]  # Keep the leading empty part or '/images'
        for part in parts[1:]:
            if part:  # Skip empty parts
                # Encode spaces and special characters
                encoded_parts.append(quote(part, safe=''))
        encoded_path = '/'.join(encoded_parts)
        return f'<img src="{encoded_path}" alt="" />'
    
    new_content = re.sub(pattern, encode_spaces, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {file_path}")
        return True
    return False

def main():
    """Fix all MDX files in Owners & Administration."""
    base_dir = Path(__file__).parent
    owners_dir = base_dir / "Owners & Administration"
    
    fixed_count = 0
    for mdx_file in owners_dir.rglob("*.mdx"):
        if fix_image_paths_in_file(mdx_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()

