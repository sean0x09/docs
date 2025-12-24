#!/usr/bin/env python3
"""
Download images from Framer URLs and update MDX files with local paths.
"""

import os
import re
import requests
from pathlib import Path

# Mapping of files to their structure
FILE_MAPPING = {
    "getting-started-with-your-practice.mdx": {
        "category": "Owners & Administration",
        "subcategory": "My Practice",
        "title": "Getting Started with Your Practice"
    },
    "your-athelas-invoice.mdx": {
        "category": "Owners & Administration",
        "subcategory": "My Practice",
        "title": "Your Athelas Invoice"
    },
    "manage-staff-permissions.mdx": {
        "category": "Owners & Administration",
        "subcategory": "My Practice",
        "title": "Manage Staff & Permissions"
    },
    "update-practice-information.mdx": {
        "category": "Owners & Administration",
        "subcategory": "My Practice",
        "title": "Update Practice Information"
    },
    "measuring-performance.mdx": {
        "category": "Owners & Administration",
        "subcategory": "Reporting",
        "title": "Measuring Performance"
    }
}

def sanitize_filename(name):
    """Convert title to sanitized filename."""
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

def download_image(url, save_path):
    """Download an image from URL to save_path."""
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, timeout=30, verify=False, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"  ✓ Downloaded: {os.path.basename(save_path)}")
        return True
    except Exception as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return False

def process_mdx_file(mdx_path, base_dir, images_dir):
    """Process an MDX file to download images and update paths."""
    filename = os.path.basename(mdx_path)
    if filename not in FILE_MAPPING:
        print(f"Skipping {filename} - not in mapping")
        return
    
    mapping = FILE_MAPPING[filename]
    sanitized_title = sanitize_filename(mapping["title"])
    
    # Read MDX file
    with open(mdx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Framer image URLs
    pattern = r'!\[\]\((https://framerusercontent\.com/images/[^)]+)\)'
    matches = list(re.finditer(pattern, content))
    
    if not matches:
        print(f"No Framer images found in {filename}")
        return
    
    print(f"\nProcessing {filename} ({len(matches)} images)")
    
    # Prepare image paths
    category_path = mapping["category"]
    subcategory_path = mapping["subcategory"]
    image_base_dir = Path(images_dir) / category_path / subcategory_path / sanitized_title
    image_base_path = f"/images/{category_path}/{subcategory_path}/{sanitized_title}"
    
    # Download images and update content
    new_content = content
    for i, match in enumerate(matches, 1):
        url = match.group(1)
        image_filename = f"{sanitized_title}-{i}.png"
        local_image_path = image_base_dir / image_filename
        local_image_url = f"{image_base_path}/{sanitized_title}-{i}.png"
        
        # Download image
        if download_image(url, local_image_path):
            # Replace URL in content
            new_content = new_content.replace(match.group(0), f'![]({local_image_url})', 1)
        else:
            print(f"  Keeping original URL for image {i}")
    
    # Write updated MDX file
    with open(mdx_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Updated {filename}")

def main():
    """Main function."""
    base_dir = Path(__file__).parent
    images_dir = base_dir / "images"
    owners_dir = base_dir / "Owners & Administration"
    
    # Process each MDX file
    for filename, mapping in FILE_MAPPING.items():
        subcategory = mapping["subcategory"]
        mdx_path = owners_dir / subcategory / filename
        
        if mdx_path.exists():
            process_mdx_file(mdx_path, base_dir, images_dir)
        else:
            print(f"File not found: {mdx_path}")

if __name__ == "__main__":
    main()

