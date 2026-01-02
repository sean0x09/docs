#!/usr/bin/env python3
"""
Script to convert onboarding documents from Framer-exported HTML to Mintlify MDX format.

Usage:
    python3 convert_onboarding_docs.py

The script will:
1. Parse .txt files from AAA-Framer-Export/Onboarding Documents/
2. Extract and download images from Framer URLs
3. Convert HTML to MDX markdown
4. Create Onboarding-Documents/ folder structure
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
    
    Paths are URL-encoded (spaces → %20, & → %26) as per rules.md requirements.
    """
    # URL-encode the path
    encoded_path = quote(local_path, safe='/')
    return f'<img src="{encoded_path}" alt="" />'

def html_to_markdown(html_content, image_tags):
    """Convert HTML to markdown, replacing images with HTML img tags."""
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
    
    # Convert headings (h2, h3, h4, h5, h6)
    html_content = re.sub(r'<h2>(.*?)</h2>', r'\n\n## \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h3>(.*?)</h3>', r'\n\n### \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h4>(.*?)</h4>', r'\n\n#### \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h5>(.*?)</h5>', r'\n\n##### \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h6>(.*?)</h6>', r'\n\n###### \1\n\n', html_content, flags=re.DOTALL)
    
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
    
    # Convert HTML tables to markdown tables
    def convert_table(match):
        table_html = match.group(0)
        rows = []
        # Extract table rows
        row_matches = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, flags=re.DOTALL)
        for row_html in row_matches:
            cells = []
            # Check if it's a header row
            is_header = '<th>' in row_html or '<th ' in row_html
            cell_tag = 'th' if is_header else 'td'
            cell_matches = re.findall(rf'<{cell_tag}[^>]*>(.*?)</{cell_tag}>', row_html, flags=re.DOTALL)
            for cell_html in cell_matches:
                # Clean up cell content
                cell_content = cell_html
                cell_content = re.sub(r'<p>(.*?)</p>', r'\1', cell_content, flags=re.DOTALL)
                cell_content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', cell_content)
                cell_content = re.sub(r'<em>(.*?)</em>', r'*\1*', cell_content)
                cell_content = re.sub(r'<code>(.*?)</code>', r'`\1`', cell_content)
                cell_content = html.unescape(cell_content).strip()
                cells.append(cell_content)
            if cells:
                rows.append(cells)
        
        if not rows:
            return match.group(0)
        
        # Build markdown table
        markdown_table = []
        # Header row
        if rows:
            header = rows[0]
            markdown_table.append('| ' + ' | '.join(header) + ' |')
            markdown_table.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
            # Data rows
            for row in rows[1:]:
                markdown_table.append('| ' + ' | '.join(row) + ' |')
        
        return '\n\n' + '\n'.join(markdown_table) + '\n\n'
    
    # Convert tables (handle both <table> and <figure><table> patterns)
    html_content = re.sub(r'<figure>\s*<table[^>]*>(.*?)</table>\s*</figure>', convert_table, html_content, flags=re.DOTALL)
    html_content = re.sub(r'<table[^>]*>(.*?)</table>', convert_table, html_content, flags=re.DOTALL)
    
    # Convert iframes (YouTube embeds) to proper Mintlify format
    def convert_iframe(match):
        src = match.group(1) if match.group(1) else ''
        # Extract YouTube video ID if it's a YouTube URL
        if 'youtube.com' in src or 'youtu.be' in src:
            # Format as Mintlify iframe
            return f'''<iframe
  className="w-full aspect-video rounded-xl"
  src="{src}"
  title="YouTube video player"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
></iframe>'''
        return match.group(0)
    
    html_content = re.sub(r'<iframe[^>]+src="([^"]+)"[^>]*>.*?</iframe>', convert_iframe, html_content, flags=re.DOTALL)
    
    # Clean up br tags
    html_content = re.sub(r'<br\s*/?>', '\n', html_content)
    html_content = re.sub(r'<br>', '\n', html_content)
    
    # Clean up extra whitespace
    html_content = re.sub(r'\n{3,}', '\n\n', html_content)
    html_content = re.sub(r'[ \t]+\n', '\n', html_content)
    
    # Remove any remaining HTML tags (preserve with comment)
    # CRITICAL: Preserve img and iframe tags - they're needed for Mintlify display
    remaining_html = re.findall(r'<[^>]+>', html_content)
    if remaining_html:
        for tag in set(remaining_html):
            # Preserve img tags, iframe tags, and common formatting tags
            if (tag.startswith('<img') or tag.startswith('<iframe') or 
                tag in ['<p>', '</p>', '<br>', '<br/>', '<ul>', '</ul>', '<ol>', '</ol>', '<li>', '</li>']):
                continue
            html_content = html_content.replace(tag, f'<!-- HTML preserved: {tag} -->')
    
    # Unescape HTML entities
    html_content = html.unescape(html_content)
    
    return html_content.strip()

def process_file(input_file, output_dir, images_dir):
    """Process a single .txt file and convert to MDX."""
    filename = os.path.basename(input_file)
    
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
    
    # Image folder: images/Onboarding-Documents/[sanitized-title]/
    image_base_dir = Path(images_dir) / "Onboarding-Documents" / sanitized_title
    image_base_path = f"/images/Onboarding-Documents/{sanitized_title}"
    
    print(f"  Processing {len(image_urls)} images...")
    for i, url in enumerate(image_urls, 1):
        image_filename = f"{sanitized_title}-{i}.png"
        local_image_path = image_base_dir / image_filename
        image_path_for_mdx = f"{image_base_path}/{sanitized_title}-{i}.png"
        
        if download_image(url, local_image_path):
            # Use HTML img tag with URL-encoded path
            image_tags.append(create_image_tag(image_path_for_mdx))
            print(f"    ✓ Downloaded: {image_filename}")
        else:
            # Keep original URL if download fails (will be converted later)
            image_tags.append(f'<img src="{url}" alt="" />')
    
    # Convert HTML to markdown (images will be replaced with HTML img tags)
    markdown_content = html_to_markdown(html_content, image_tags)
    
    # Create output directory
    output_path = Path(output_dir) / "Onboarding-Documents"
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

def main():
    """Main conversion function."""
    base_dir = Path(__file__).parent
    input_dir = base_dir / "AAA-Framer-Export" / "Onboarding Documents"
    output_dir = base_dir
    images_dir = base_dir / "images"
    
    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}")
        return
    
    # Find all .txt files in the onboarding documents folder
    txt_files = list(input_dir.glob("*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {input_dir}")
        return
    
    print(f"Found {len(txt_files)} onboarding document(s) to process\n")
    
    processed = 0
    for txt_file in txt_files:
        print(f"Processing: {txt_file.name}")
        if process_file(txt_file, output_dir, images_dir):
            processed += 1
        print()
    
    print(f"Completed: {processed}/{len(txt_files)} files processed")

if __name__ == "__main__":
    main()

