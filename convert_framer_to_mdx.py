#!/usr/bin/env python3
"""
Universal script to convert Framer-exported HTML documents to Mintlify MDX format.
Handles all workflow categories: Provider, Front Office, Billing, and Owners & Administration.

Usage:
    python3 convert_framer_to_mdx.py <category>
    
Categories: owners-admin, provider, front-office, billing, all

The script will:
1. Parse .txt files from AAA-Framer-Export/
2. Extract and download images from Framer URLs
3. Convert HTML to MDX markdown
4. Create proper folder structure matching IA
5. Generate MDX files with frontmatter
6. Use HTML img tags with URL-encoded paths for proper image display
"""

import os
import re
import requests
from pathlib import Path
from html import unescape
import html
from urllib.parse import quote
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sanitize_filename(name):
    """Convert title to sanitized filename."""
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

def extract_images(html_content):
    """Extract all image URLs from HTML content."""
    pattern = r'<img[^>]+src="(https://framerusercontent\.com/images/[^"]+)"'
    images = re.findall(pattern, html_content)
    return images

def download_image(url, save_path):
    """Download an image from URL to save_path."""
    try:
        response = requests.get(url, timeout=30, verify=False, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"    ✗ Error downloading {url}: {e}")
        return False

def create_image_tag(local_path):
    """Create HTML img tag with URL-encoded path for Mintlify compatibility.
    
    CRITICAL: Mintlify requires URL-encoded paths in HTML img tags when folder names contain spaces.
    This ensures images display correctly instead of showing as plain text.
    """
    # URL-encode the path properly - encode spaces and special chars but keep slashes
    parts = local_path.split('/')
    encoded_parts = [parts[0]]  # Keep the leading empty part or '/images'
    for part in parts[1:]:
        if part:  # Skip empty parts
            # Encode spaces (%20) and special characters like & (%26)
            encoded_parts.append(quote(part, safe=''))
    encoded_path = '/'.join(encoded_parts)
    return f'<img src="{encoded_path}" alt="" />'

def html_to_markdown(html_content, image_tags):
    """Convert HTML to markdown, replacing images with HTML img tags.
    
    IMPORTANT: Images are replaced with HTML img tags (not markdown syntax) because:
    1. Mintlify handles URL-encoded paths better in HTML tags
    2. Spaces in folder names require URL encoding which works better in HTML
    """
    # Replace images first - need to track which image we're on
    image_index = 0
    
    def replace_img(match):
        nonlocal image_index
        if image_index < len(image_tags):
            tag = image_tags[image_index]
            image_index += 1
            return f'\n\n{tag}\n\n'
        return match.group(0)
    
    # Replace img tags (handle both with and without alt)
    html_content = re.sub(r'<img[^>]+>', replace_img, html_content)
    
    # Convert headings
    html_content = re.sub(r'<h3>(.*?)</h3>', r'\n\n### \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h4>(.*?)</h4>', r'\n\n#### \1\n\n', html_content, flags=re.DOTALL)
    
    # Convert nested lists - process from innermost to outermost
    def process_lists(text):
        max_depth = 10
        for d in range(max_depth, 0, -1):
            pattern = r'(<li[^>]*>)(.*?)(</li>)'
            def replace_li(match):
                content = match.group(2)
                if '<ul>' in content or '<ol>' in content:
                    content = process_lists(content)
                    return f'- {content}\n'
                else:
                    content = re.sub(r'<p>(.*?)</p>', r'\1', content, flags=re.DOTALL)
                    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
                    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
                    content = re.sub(r'<code>(.*?)</code>', r'`\1`', content)
                    content = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
                    content = html.unescape(content).strip()
                    return f'- {content}\n'
            
            text = re.sub(pattern, replace_li, text, flags=re.DOTALL)
        
        text = re.sub(r'</?ul[^>]*>', '', text)
        text = re.sub(r'</?ol[^>]*>', '', text)
        return text
    
    html_content = process_lists(html_content)
    
    # Convert paragraphs (but not those already in lists)
    html_content = re.sub(r'<p>(.*?)</p>', r'\1\n\n', html_content, flags=re.DOTALL)
    
    # Convert strong and em
    html_content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html_content)
    html_content = re.sub(r'<em>(.*?)</em>', r'*\1*', html_content)
    
    # Convert code
    html_content = re.sub(r'<code>(.*?)</code>', r'`\1`', html_content)
    
    # Convert links
    html_content = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', html_content)
    
    # Clean up br tags
    html_content = re.sub(r'<br\s*/?>', '\n', html_content)
    html_content = re.sub(r'<br>', '\n', html_content)
    
    # Clean up extra whitespace
    html_content = re.sub(r'\n{3,}', '\n\n', html_content)
    html_content = re.sub(r'[ \t]+\n', '\n', html_content)
    
    # Remove any remaining HTML tags (preserve with comment)
    remaining_html = re.findall(r'<[^>]+>', html_content)
    if remaining_html:
        for tag in set(remaining_html):
            if tag not in ['<p>', '</p>', '<br>', '<br/>', '<ul>', '</ul>', '<ol>', '</ol>', '<li>', '</li>']:
                html_content = html_content.replace(tag, f'<!-- HTML preserved: {tag} -->')
    
    # Unescape HTML entities
    html_content = html.unescape(html_content)
    
    return html_content.strip()

def process_file(input_file, file_mapping, output_dir, images_dir):
    """Process a single .txt file and convert to MDX."""
    filename = os.path.basename(input_file)
    if filename not in file_mapping:
        return False
    
    mapping = file_mapping[filename]
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        print(f"  ✗ Skipping {filename} - invalid format")
        return False
    
    title = lines[0].strip()
    html_content = ''.join(lines[2:])  # Skip title and empty line
    
    # Extract images
    image_urls = extract_images(html_content)
    
    # Create image paths and download
    sanitized_title = sanitize_filename(title)
    image_tags = []
    
    category_path = mapping["category"]
    subcategory_path = mapping["subcategory"]
    image_base_dir = Path(images_dir) / category_path / subcategory_path / sanitized_title
    image_base_path = f"/images/{category_path}/{subcategory_path}/{sanitized_title}"
    
    print(f"  Processing {len(image_urls)} images...")
    for i, url in enumerate(image_urls, 1):
        image_filename = f"{sanitized_title}-{i}.png"
        local_image_path = image_base_dir / image_filename
        image_path_for_mdx = f"{image_base_path}/{sanitized_title}-{i}.png"
        
        if download_image(url, local_image_path):
            # Use HTML img tag with URL-encoded path (CRITICAL for Mintlify)
            image_tags.append(create_image_tag(image_path_for_mdx))
            print(f"    ✓ Downloaded: {image_filename}")
        else:
            # Keep original URL if download fails (will be converted later)
            image_tags.append(f'<img src="{url}" alt="" />')
    
    # Convert HTML to markdown (images will be replaced with HTML img tags)
    markdown_content = html_to_markdown(html_content, image_tags)
    
    # Create output directory
    output_path = Path(output_dir) / category_path / subcategory_path
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Write MDX file
    mdx_filename = f"{sanitized_title}.mdx"
    mdx_path = output_path / mdx_filename
    
    with open(mdx_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(f'title: "{title}"\n')
        f.write('---\n\n')
        f.write(markdown_content)
    
    print(f"  ✓ Created: {mdx_path}")
    return True

def load_file_mapping(category):
    """Load file mapping for a specific category.
    
    File mappings should be defined based on the IA structure in .cursor/rules.md.
    Each entry maps the .txt filename to its category, subcategory, and title.
    
    To add mappings for a new category:
    1. Look up the IA structure in .cursor/rules.md
    2. For each file in that category, add an entry mapping the .txt filename
    3. Use the exact category and subcategory names from the IA
    4. Use the exact title from the first line of the .txt file
    """
    mappings = {
        "owners-admin": {
            "Getting Started with Your Practice.txt": {
                "category": "Owners & Administration",
                "subcategory": "My Practice",
                "title": "Getting Started with Your Practice"
            },
            "Your Athelas Invoice.txt": {
                "category": "Owners & Administration",
                "subcategory": "My Practice",
                "title": "Your Athelas Invoice"
            },
            "Manage Staff & Permissions.txt": {
                "category": "Owners & Administration",
                "subcategory": "My Practice",
                "title": "Manage Staff & Permissions"
            },
            "Update Practice Information.txt": {
                "category": "Owners & Administration",
                "subcategory": "My Practice",
                "title": "Update Practice Information"
            },
            "Measuring Performance.txt": {
                "category": "Owners & Administration",
                "subcategory": "Reporting",
                "title": "Measuring Performance"
            }
        },
        # Add mappings for other categories here:
        # "provider": { ... },
        # "front-office": { ... },
        # "billing": { ... },
    }
    
    return mappings.get(category, {})

def main():
    """Main conversion function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 convert_framer_to_mdx.py <category>")
        print("\nCategories:")
        print("  owners-admin    - Owners & Administration")
        print("  provider        - Provider Workflows")
        print("  front-office    - Front Office Workflows")
        print("  billing         - Billing Workflows")
        print("  all             - All categories")
        print("\nNote: File mappings must be defined in load_file_mapping() function")
        print("based on the IA structure in .cursor/rules.md")
        sys.exit(1)
    
    category_arg = sys.argv[1].lower()
    
    base_dir = Path(__file__).parent
    input_dir = base_dir / "AAA-Framer-Export"
    output_dir = base_dir
    images_dir = base_dir / "images"
    
    # Load file mapping for the category
    file_mapping = load_file_mapping(category_arg)
    
    if not file_mapping:
        print(f"ERROR: No file mapping defined for category '{category_arg}'")
        print("Please define the file mapping in load_file_mapping() function")
        print("based on the IA structure in .cursor/rules.md")
        sys.exit(1)
    
    print(f"Processing category: {category_arg}")
    print(f"Found {len(file_mapping)} files to process\n")
    
    processed = 0
    for filename, mapping in file_mapping.items():
        input_file = input_dir / filename
        if input_file.exists():
            print(f"Processing: {filename}")
            if process_file(input_file, file_mapping, output_dir, images_dir):
                processed += 1
            print()
        else:
            print(f"✗ File not found: {input_file}\n")
    
    print(f"Completed: {processed}/{len(file_mapping)} files processed")

if __name__ == "__main__":
    main()
