#!/usr/bin/env python3
"""
Convert Owners & Administration Framer HTML files to Mintlify MDX format.
"""

import os
import re
import requests
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import html

# Mapping of files to their IA structure
FILE_MAPPING = {
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
}

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
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def html_to_markdown(html_content, image_paths):
    """Convert HTML to markdown, replacing images with local paths."""
    # Replace images first - need to track which image we're on
    image_index = 0
    
    def replace_img(match):
        nonlocal image_index
        if image_index < len(image_paths):
            alt_match = re.search(r'alt="([^"]*)"', match.group(0))
            alt = alt_match.group(1) if alt_match else ""
            path = image_paths[image_index]
            image_index += 1
            return f'\n\n![{alt}]({path})\n\n'
        return match.group(0)
    
    # Replace img tags (handle both with and without alt)
    html_content = re.sub(r'<img[^>]+>', replace_img, html_content)
    
    # Convert headings
    html_content = re.sub(r'<h3>(.*?)</h3>', r'\n\n### \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h4>(.*?)</h4>', r'\n\n#### \1\n\n', html_content, flags=re.DOTALL)
    
    # Convert nested lists - process from innermost to outermost
    # Handle nested ul/ol structures
    def process_lists(text):
        # Process nested lists by replacing inner lists first
        depth = 0
        max_depth = 10
        for d in range(max_depth, 0, -1):
            # Find list items at this depth
            pattern = r'(<li[^>]*>)(.*?)(</li>)'
            def replace_li(match):
                content = match.group(2)
                # Check if this li contains nested lists
                if '<ul>' in content or '<ol>' in content:
                    # Process nested content
                    content = process_lists(content)
                    return f'- {content}\n'
                else:
                    # Simple list item
                    content = re.sub(r'<p>(.*?)</p>', r'\1', content, flags=re.DOTALL)
                    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
                    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
                    content = re.sub(r'<code>(.*?)</code>', r'`\1`', content)
                    content = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
                    content = html.unescape(content).strip()
                    return f'- {content}\n'
            
            text = re.sub(pattern, replace_li, text, flags=re.DOTALL)
        
        # Remove ul/ol tags
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

def process_file(input_file, output_dir, images_dir):
    """Process a single file."""
    filename = os.path.basename(input_file)
    if filename not in FILE_MAPPING:
        print(f"Skipping {filename} - not in mapping")
        return
    
    mapping = FILE_MAPPING[filename]
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    title = lines[0].strip()
    html_content = ''.join(lines[2:])  # Skip title and empty line
    
    # Extract images
    image_urls = extract_images(html_content)
    
    # Create image paths and download
    sanitized_title = sanitize_filename(title)
    image_paths = []
    
    category_path = mapping["category"]
    subcategory_path = mapping["subcategory"]
    image_base_path = f"/images/{category_path}/{subcategory_path}/{sanitized_title}"
    
    for i, url in enumerate(image_urls, 1):
        image_filename = f"{sanitized_title}-{i}.png"
        local_image_path = os.path.join(images_dir, category_path, subcategory_path, sanitized_title, image_filename)
        image_path_for_mdx = f"{image_base_path}/{sanitized_title}-{i}.png"
        
        if download_image(url, local_image_path):
            image_paths.append(image_path_for_mdx)
            print(f"Downloaded: {image_filename}")
        else:
            # Keep original URL if download fails
            image_paths.append(url)
    
    # Convert HTML to markdown
    markdown_content = html_to_markdown(html_content, image_paths)
    
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
    
    print(f"Created: {mdx_path}")

def main():
    """Main conversion function."""
    base_dir = Path(__file__).parent
    input_dir = base_dir / "AAA-Framer-Export"
    output_dir = base_dir
    images_dir = base_dir / "images"
    
    # Process each file
    for filename in FILE_MAPPING.keys():
        input_file = input_dir / filename
        if input_file.exists():
            print(f"\nProcessing: {filename}")
            process_file(input_file, output_dir, images_dir)
        else:
            print(f"File not found: {input_file}")

if __name__ == "__main__":
    main()

