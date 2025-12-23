#!/usr/bin/env python3
"""
Script to download images for organized documentation files.
Extracts image URLs from files and downloads them to the correct locations.
"""

import os
import re
import requests
from pathlib import Path
from urllib3.util.ssl_ import create_urllib3_context
import ssl

# Disable SSL verification warnings (use with caution)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_image_urls(content: str) -> list:
    """Extract image URLs from HTML content."""
    pattern = r'<img[^>]+src="([^"]+)"'
    urls = re.findall(pattern, content)
    # Filter for framerusercontent.com URLs
    return [url for url in urls if 'framerusercontent.com' in url]

def sanitize_title(title: str) -> str:
    """Sanitize title for use in filenames and folder names."""
    title = title.lower()
    title = title.replace(" ", "-")
    title = re.sub(r'[^a-z0-9\-]', '', title)
    title = re.sub(r'-+', '-', title)
    title = title.strip('-')
    return title

def download_image(url: str, filepath: Path) -> bool:
    """Download image from URL to filepath."""
    try:
        # Create a session with SSL verification disabled
        session = requests.Session()
        session.verify = False
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = session.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        
        # Determine file extension from URL or content type
        ext = '.png'
        if url.endswith('.gif'):
            ext = '.gif'
        elif url.endswith('.jpg') or url.endswith('.jpeg'):
            ext = '.jpg'
        elif 'content-type' in response.headers:
            content_type = response.headers['content-type']
            if 'gif' in content_type:
                ext = '.gif'
            elif 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
        
        # Update filepath with correct extension
        if not filepath.suffix or filepath.suffix != ext:
            filepath = filepath.with_suffix(ext)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False

def process_file(file_path: Path, images_dir: Path, log_file):
    """Process a single file to download its images."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            return False
        
        # Extract title (first line)
        title = lines[0].strip()
        content = ''.join(lines[1:]) if len(lines) > 1 else ''
        
        # Extract image URLs
        image_urls = extract_image_urls(content)
        
        if not image_urls:
            return True  # No images to download
        
        # Sanitize title for folder/filename
        sanitized_title = sanitize_title(title)
        
        # Create image folder
        image_folder = images_dir / sanitized_title
        image_folder.mkdir(parents=True, exist_ok=True)
        
        # Download images
        downloaded = 0
        for i, url in enumerate(image_urls, 1):
            # Determine extension from URL
            ext = '.png'
            if url.endswith('.gif'):
                ext = '.gif'
            elif url.endswith('.jpg') or url.endswith('.jpeg'):
                ext = '.jpg'
            
            image_filename = f"{sanitized_title}-{i}{ext}"
            image_path = image_folder / image_filename
            
            if download_image(url, image_path):
                downloaded += 1
                log_file.write(f"  Downloaded: {image_filename}\n")
            else:
                log_file.write(f"  Failed: {image_filename} from {url}\n")
        
        log_file.write(f"PROCESSED: {file_path.name} - Downloaded {downloaded}/{len(image_urls)} images\n")
        return True
        
    except Exception as e:
        log_file.write(f"ERROR: {file_path.name} - {str(e)}\n")
        return False

def main():
    """Main function to download images for all organized files."""
    base_dir = Path(__file__).parent
    images_dir = base_dir / "images"
    source_dir = base_dir / "DELETE-Framer-Doc"
    log_path = base_dir / "image_download_log.txt"
    
    # Read from original files in DELETE-Framer-Doc to get the original URLs
    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} not found")
        return
    
    txt_files = list(source_dir.glob("*.txt"))
    print(f"Found {len(txt_files)} source files to process")
    
    processed = 0
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Image Download Log\n")
        log_file.write("=" * 50 + "\n\n")
        
        for i, file_path in enumerate(txt_files, 1):
            print(f"Processing {i}/{len(txt_files)}: {file_path.name}")
            # Extract title to match with organized files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    title = f.readline().strip()
                print(f"  Title: {title}")
            except:
                title = file_path.stem
            
            if process_file(file_path, images_dir, log_file):
                processed += 1
    
    print(f"\nProcessed {processed}/{len(txt_files)} files")
    print(f"Log saved to {log_path}")

if __name__ == "__main__":
    main()

