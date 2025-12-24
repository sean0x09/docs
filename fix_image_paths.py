#!/usr/bin/env python3
"""
Fix image paths in MDX files by URL-encoding spaces.
"""

import os
import re
from pathlib import Path
from urllib.parse import quote

def fix_image_paths_in_file(file_path):
    """Fix image paths in a single MDX file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image markdown syntax with paths containing spaces
    pattern = r'!\[\]\((/images/[^)]+)\)'
    
    def encode_path(match):
        path = match.group(1)
        # URL-encode the path, but keep the leading slash and forward slashes
        # Only encode spaces and special characters
        encoded_path = '/images/' + '/'.join(quote(part, safe='') for part in path.replace('/images/', '').split('/'))
        return f'![]({encoded_path})'
    
    new_content = re.sub(pattern, encode_path, content)
    
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

