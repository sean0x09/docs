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
    # CRITICAL: Preserve img tags - they're needed for Mintlify image display
    remaining_html = re.findall(r'<[^>]+>', html_content)
    if remaining_html:
        for tag in set(remaining_html):
            # Preserve img tags and common formatting tags
            if tag.startswith('<img') or tag in ['<p>', '</p>', '<br>', '<br/>', '<ul>', '</ul>', '<ol>', '</ol>', '<li>', '</li>']:
                continue
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
    
    File mappings are defined based on the IA structure in .cursor/rules.md.
    Each entry maps the .txt filename to its category, subcategory, and title.
    
    Note on duplicate files:
    Some files appear in multiple categories in the IA (e.g., "Getting started with the Calendar"
    appears in both Provider and Front Office Workflows). These are kept in the Front Office
    mapping to avoid conflicts. If needed in multiple locations, create symlinks or update
    docs.json navigation to reference the same file from multiple places.
    
    Mapping coverage:
    - Total files in AAA-Framer-Export/: 178
    - Files mapped in this function: 168
    - Unmapped files: 10 (see .cursor/rules.md "Files Not in IA" section)
    
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
        "provider": {
            # Chart Notes
            "Getting Started with Chart Notes.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Getting Started with Chart Notes"
            },
            "Auto-apply KX Modifier.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Auto-apply KX Modifier"
            },
            "AI Appt. Summaries.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "AI Appt. Summaries"
            },
            "Chart Note Clinical Types.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Chart Note Clinical Types"
            },
            "Download Chart Notes as PDFs.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Download Chart Notes as PDFs"
            },
            "Goals on the chart note.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Goals on the chart note"
            },
            "How to add Measurements.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "How to add Measurements"
            },
            "Import Previous Medical History.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Import Previous Medical History"
            },
            "Navigating Flowsheets.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Navigating Flowsheets"
            },
            "Navigating Inbox Workflows.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Navigating Inbox Workflows"
            },
            "Navigating the Chart Note.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Navigating the Chart Note"
            },
            "Set up Custom Chart Note Templates.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Set up Custom Chart Note Templates"
            },
            "Setting up Co-signers on Your Note.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Setting up Co-signers on Your Note"
            },
            "Sign a Chart Note.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Sign a Chart Note"
            },
            "Text Snippets For Your Note.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Text Snippets For Your Note"
            },
            "Chart Note Features Not Supported.txt": {
                "category": "Provider Workflows",
                "subcategory": "Chart Notes",
                "title": "Chart Note Features Not Supported"
            },
            # AI Scribe & Tooling
            "Additional Context Feature.txt": {
                "category": "Provider Workflows",
                "subcategory": "AI Scribe & Tooling",
                "title": "Additional Context Feature"
            },
            "Complete a Visit with Air Scribe.txt": {
                "category": "Provider Workflows",
                "subcategory": "AI Scribe & Tooling",
                "title": "Complete a Visit with Air Scribe"
            },
            "Edit with Command+K.txt": {
                "category": "Provider Workflows",
                "subcategory": "AI Scribe & Tooling",
                "title": "Edit with Command+K"
            },
            "How to Apply an Air Scribe.txt": {
                "category": "Provider Workflows",
                "subcategory": "AI Scribe & Tooling",
                "title": "How to Apply an Air Scribe"
            },
            "How to Set up AI Compliance.txt": {
                "category": "Provider Workflows",
                "subcategory": "AI Scribe & Tooling",
                "title": "How to Set up AI Compliance"
            },
            "Setting up AI Compliance.txt": {
                "category": "Provider Workflows",
                "subcategory": "AI Scribe & Tooling",
                "title": "Setting up AI Compliance"
            },
            # Calendar
            # Note: "Getting started with the Calendar" and "Filter the calendar view" 
            # appear in both Provider and Front Office Workflows in the IA.
            # They are kept in Front Office Workflows mapping to avoid duplicates.
            # If needed in Provider location, create symlinks or update docs.json navigation.
            # Claim Details  
            # Note: "Submissions and Remits" appears in both Provider and Front Office Workflows.
            # It is kept in Front Office Workflows mapping to avoid duplicates.
            # Patient Profiles
            "Getting started with Patient Profile.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "Getting started with Patient Profile"
            },
            "Navigating Labs.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "Navigating Labs"
            },
            "Add attachments to Patient Profile.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "Add attachments to Patient Profile"
            },
            "Prescribe Medications.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "Prescribe Medications"
            },
            "Record Allergies.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "Record Allergies"
            },
            "Record Immunizations.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "Record Immunizations"
            },
            "View Patient's Appointments.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "View Patient's Appointments"
            },
            "Profile Features Not Supported.txt": {
                "category": "Provider Workflows",
                "subcategory": "Patient Profiles",
                "title": "Profile Features Not Supported"
            },
            # Medications
            "Designate Staff as Provider Agents.txt": {
                "category": "Provider Workflows",
                "subcategory": "Medications",
                "title": "Designate Staff as Provider Agents"
            },
            # Athelas Assistant
            "Getting Started with Athelas Assistant.txt": {
                "category": "Provider Workflows",
                "subcategory": "Athelas Assistant",
                "title": "Getting Started with Athelas Assistant"
            },
            "Athelas Assistant Common Functionalities.txt": {
                "category": "Provider Workflows",
                "subcategory": "Athelas Assistant",
                "title": "Athelas Assistant Common Functionalities"
            },
            "Athelas Assistant Best Practices.txt": {
                "category": "Provider Workflows",
                "subcategory": "Athelas Assistant",
                "title": "Athelas Assistant Best Practices"
            }
        },
        "front-office": {
            # Calendar
            "Getting started with the Calendar.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Calendar",
                "title": "Getting started with the Calendar"
            },
            "Calendar start & end times.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Calendar",
                "title": "Calendar start & end times"
            },
            "Filter the calendar view.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Calendar",
                "title": "Filter the calendar view"
            },
            "Modify calendar views.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Calendar",
                "title": "Modify calendar views"
            },
            "Viewing multiple providers.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Calendar",
                "title": "Viewing multiple providers"
            },
            "Features not supported.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Calendar",
                "title": "Features not supported"
            },
            # Appointments
            "The Insights Appointments Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "The Insights Appointments Page"
            },
            "Adding Prior Auth and Alerting.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "Adding Prior Auth and Alerting"
            },
            "Alternate Methods for Scheduling.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "Alternate Methods for Scheduling"
            },
            "How to Add a Walk-In Patient.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "How to Add a Walk-In Patient"
            },
            "How to Run an Eligibility Check.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "How to Run an Eligibility Check"
            },
            "How to Schedule an Appointment.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "How to Schedule an Appointment"
            },
            "How to Take Payments.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "How to Take Payments"
            },
            "Sending out reminders and forms.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "Sending out reminders and forms"
            },
            "Understanding Appointment Details.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "Understanding Appointment Details"
            },
            "Updating Appointment Statuses.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "Updating Appointment Statuses"
            },
            "Appt. Features not supported.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Appointments",
                "title": "Appt. Features not supported"
            },
            # Agents Center
            "Getting Started with Agents Center.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Agents Center",
                "title": "Getting Started with Agents Center"
            },
            "Components of the Dashboard.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Agents Center",
                "title": "Components of the Dashboard"
            },
            "Make an Outbound Call.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Agents Center",
                "title": "Make an Outbound Call"
            },
            "Understanding Use Cases.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Agents Center",
                "title": "Understanding Use Cases"
            },
            # Claim Details
            "Claim Details Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "Claim Details Page"
            },
            "Other Submission Types (Secondary, Specialty etc).txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "Other Submission Types (Secondary, Specialty etc)"
            },
            "Encounter Timeline for Claims.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "Encounter Timeline for Claims"
            },
            "How to Download CMS-1500 Forms.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "How to Download CMS-1500 Forms"
            },
            "How to Resubmit a Single Claim.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "How to Resubmit a Single Claim"
            },
            "How to Resubmit Claims in Bulk.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "How to Resubmit Claims in Bulk"
            },
            "How to Send Documentation.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "How to Send Documentation"
            },
            "Submissions and Remits.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Claim Details",
                "title": "Submissions and Remits"
            },
            # Daily Operations
            "How to Reconcile Your Cash Drawer.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Daily Operations",
                "title": "How to Reconcile Your Cash Drawer"
            },
            # Encounter Details
            "Encounter Details Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Encounter Details",
                "title": "Encounter Details Page"
            },
            "Insights Prior Authorization.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Encounter Details",
                "title": "Insights Prior Authorization"
            },
            "Encounter Stage and Status.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Encounter Details",
                "title": "Encounter Stage and Status"
            },
            "How to Update Insurance.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Encounter Details",
                "title": "How to Update Insurance"
            },
            # Faxing
            "Getting Started with Faxing.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Faxing",
                "title": "Getting Started with Faxing"
            },
            "Attach Task Follow-ups to Faxes.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Faxing",
                "title": "Attach Task Follow-ups to Faxes"
            },
            "Send and Receive a Fax.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Faxing",
                "title": "Send and Receive a Fax"
            },
            "Tying Faxes to Patients.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Faxing",
                "title": "Tying Faxes to Patients"
            },
            "Tying inbound faxes to outbound faxes.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Faxing",
                "title": "Tying inbound faxes to outbound faxes"
            },
            "Faxing Features Not Supported.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Faxing",
                "title": "Faxing Features Not Supported"
            },
            # Messaging
            "How to receive messages.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Messaging",
                "title": "How to receive messages"
            },
            "How to send messages.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Messaging",
                "title": "How to send messages"
            },
            "Messages Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Messaging",
                "title": "Messages Page"
            },
            # Patient Communications
            "General Patient Flows Features.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "General Patient Flows Features"
            },
            "Text Blast Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Text Blast Page"
            },
            "Insurance Intake Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Insurance Intake Page"
            },
            "Functional Outcome Measurements.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Functional Outcome Measurements"
            },
            "Getting Started with Patient Portal.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Getting Started with Patient Portal"
            },
            "Complete Intake Forms.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Complete Intake Forms"
            },
            "Navigating Patient Workflows.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Navigating Patient Workflows"
            },
            "Manage Patient Appointments.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Manage Patient Appointments"
            },
            "Manage Payments through Patient Portal.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Manage Payments through Patient Portal"
            },
            "Patient Intake Automation.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Patient Intake Automation"
            },
            "Update Insurance Info.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "Update Insurance Info"
            },
            "View Home Exercise Programs.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Communications",
                "title": "View Home Exercise Programs"
            },
            # Patient Demographics
            "Getting Started with Demographics.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Demographics",
                "title": "Getting Started with Demographics"
            },
            "Add_edit a Patient's Insurance.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Demographics",
                "title": "Add/edit a Patient's Insurance"
            },
            "Add_edit Patient Cases.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Demographics",
                "title": "Add/edit Patient Cases"
            },
            "Add_edit Patient's Prior Authorization.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Demographics",
                "title": "Add/edit Patient's Prior Authorization"
            },
            # Patient Profiles
            "How to Find and Edit a Patient's Profile.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Profiles",
                "title": "How to Find and Edit a Patient's Profile"
            },
            "How to Resubmit Claim(s).txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Profiles",
                "title": "How to Resubmit Claim(s)"
            },
            # Patient Responsibility
            "Patient Responsibility Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "Patient Responsibility Page"
            },
            "Charge Saved Credit Cards.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "Charge Saved Credit Cards"
            },
            "Manage Credit Cards.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "Manage Credit Cards"
            },
            "Setting up a Payment Plan.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "Setting up a Payment Plan"
            },
            "How to Cancel PR.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Cancel PR"
            },
            "How to Send a Patient Payment Link.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Send a Patient Payment Link"
            },
            "How to Push to PR.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Push to PR"
            },
            "How to Record Payments.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Record Payments"
            },
            "How to Refund a Payment.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Refund a Payment"
            },
            "How to Request via Text or Email.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Request via Text or Email"
            },
            "How to Set Up Miscellaneous Line Item Charges.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Set Up Miscellaneous Line Item Charges"
            },
            "How to Take Payment for Families.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Take Payment for Families"
            },
            "How to Undo a Write Off.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Undo a Write Off"
            },
            "How to Write Off PR.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "How to Write Off PR"
            },
            "PR Overpayment Refunds and Estimated vs. Remittance PR.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "PR Overpayment Refunds and Estimated vs. Remittance PR"
            },
            "PR Settings.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "PR Settings"
            },
            "PR Timeline.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Responsibility",
                "title": "PR Timeline"
            },
            # Patient Statements
            "Turn off Patient Texts.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Statements",
                "title": "Turn off Patient Texts"
            },
            "How to Spread PR Statement Emails.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Statements",
                "title": "How to Spread PR Statement Emails"
            },
            "Manage Patient Statements.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Statements",
                "title": "Manage Patient Statements"
            },
            "Print Patient Statements.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Statements",
                "title": "Print Patient Statements"
            },
            "Send Email Statements.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Statements",
                "title": "Send Email Statements"
            },
            "Send One-off Paper Statements.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Statements",
                "title": "Send One-off Paper Statements"
            },
            "Send Patient Statements via Email_Text.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Patient Statements",
                "title": "Send Patient Statements via Email/Text"
            },
            # Posting
            "How to Handle Duplicate Remittances.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Posting",
                "title": "How to Handle Duplicate Remittances"
            },
            "How to Handle Partial Denials.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Posting",
                "title": "How to Handle Partial Denials"
            },
            "How to Post a Remittance Manually.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Posting",
                "title": "How to Post a Remittance Manually"
            },
            "How to Use the Posting Tool Page.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Posting",
                "title": "How to Use the Posting Tool Page"
            },
            "How to Write Off a Balance.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Posting",
                "title": "How to Write Off a Balance"
            },
            # Tasking
            "How to create tasks.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Tasking",
                "title": "How to create tasks"
            },
            "Sorting, Archiving, Bulk Actions.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Tasking",
                "title": "Sorting, Archiving, Bulk Actions"
            },
            # Utilities
            "Self-service Credentialing.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Utilities",
                "title": "Self-service Credentialing"
            },
            "Patient Subscriptions.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Utilities",
                "title": "Patient Subscriptions"
            },
            "Process Virtual Cards.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Utilities",
                "title": "Process Virtual Cards"
            },
            "Download EDI's in Bulk.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Utilities",
                "title": "Download EDI's in Bulk"
            },
            "Bank Deposit Verification.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Utilities",
                "title": "Bank Deposit Verification"
            },
            "EOB Creation and Portal Checks.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Utilities",
                "title": "EOB Creation and Portal Checks"
            },
            # Athelas Assistant
            "Getting Started With Your RCM Assistant.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Athelas Assistant",
                "title": "Getting Started With Your RCM Assistant"
            },
            "RCM AI Prompt Library.txt": {
                "category": "Front Office Workflows",
                "subcategory": "Athelas Assistant",
                "title": "RCM AI Prompt Library"
            }
        },
        "billing": {
            # Analytics
            "The Denials Analysis Page.txt": {
                "category": "Billing Workflows",
                "subcategory": "Analytics",
                "title": "The Denials Analysis Page"
            },
            "The Revenue Analysis Page.txt": {
                "category": "Billing Workflows",
                "subcategory": "Analytics",
                "title": "The Revenue Analysis Page"
            },
            # Front Office Payments
            "How to Create Suggested PR Rules.txt": {
                "category": "Billing Workflows",
                "subcategory": "Front Office Payments",
                "title": "How to Create Suggested PR Rules"
            },
            "Self-pay Fee Schedule.txt": {
                "category": "Billing Workflows",
                "subcategory": "Front Office Payments",
                "title": "Self-pay Fee Schedule"
            },
            "Target Allowed Amounts.txt": {
                "category": "Billing Workflows",
                "subcategory": "Front Office Payments",
                "title": "Target Allowed Amounts"
            },
            # General Billing
            "Remittances.txt": {
                "category": "Billing Workflows",
                "subcategory": "General Billing",
                "title": "Remittances"
            },
            "How to Set Block PR Rules.txt": {
                "category": "Billing Workflows",
                "subcategory": "General Billing",
                "title": "How to Set Block PR Rules"
            },
            "The Billing Rules Engine.txt": {
                "category": "Billing Workflows",
                "subcategory": "General Billing",
                "title": "The Billing Rules Engine"
            },
            "The Review Charges Page.txt": {
                "category": "Billing Workflows",
                "subcategory": "General Billing",
                "title": "The Review Charges Page"
            },
            # Reports
            "Building and Running Reports.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Building and Running Reports"
            },
            "A_R Reports.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "A/R Reports"
            },
            "Claim Adjustments Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Claim Adjustments Report"
            },
            "Collections Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Collections Report"
            },
            "Custom Collections Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Custom Collections Report"
            },
            "Detailed Charges Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Detailed Charges Report"
            },
            "Export Claim Details.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Export Claim Details"
            },
            "Generate a Transaction Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Generate a Transaction Report"
            },
            "Patient Balances Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Patient Balances Report"
            },
            "Patient Charges Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Patient Charges Report"
            },
            "Patient Claims One-pagers.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Patient Claims One-pagers"
            },
            "Patient Collections Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Patient Collections Report"
            },
            "Patient Eligibility Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Patient Eligibility Report"
            },
            "Posting Log Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Posting Log Report"
            },
            "Site Transaction Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Site Transaction Report"
            },
            "Site Transaction Report Summary.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Site Transaction Report Summary"
            },
            "Submitted Claims Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Submitted Claims Report"
            },
            "Upcoming Patient Statements Report.txt": {
                "category": "Billing Workflows",
                "subcategory": "Reports",
                "title": "Upcoming Patient Statements Report"
            },
            # Athelas Assistant
            "Getting Started With Your RCM Assistant.txt": {
                "category": "Billing Workflows",
                "subcategory": "Athelas Assistant",
                "title": "Getting Started With Your RCM Assistant"
            },
            "RCM AI Prompt Library.txt": {
                "category": "Billing Workflows",
                "subcategory": "Athelas Assistant",
                "title": "RCM AI Prompt Library"
            }
        }
    }
    
    # Handle "all" category by merging all mappings
    if category == "all":
        all_mappings = {}
        for cat_mappings in mappings.values():
            all_mappings.update(cat_mappings)
        return all_mappings
    
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
