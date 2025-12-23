#!/usr/bin/env python3
"""
Script to organize Athelas RCM documentation files and download images.
"""

import os
import re
import json
import shutil
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher

# Information Architecture Mapping
ARCHITECTURE = {
    "Provider Workflows": {
        "Chart Notes": [
            "Getting Started with Chart Notes",
            "Auto-apply KX Modifier",
            "AI Appt. Summaries",
            "Chart Note Clinical Types",
            "Download Chart Notes as PDFs",
            "Goals on the chart note",
            "How to add Measurements",
            "Import Previous Medical History",
            "Navigating Flowsheets",
            "Navigating Inbox Workflows",
            "Navigating the Chart Note",
            "Set up Custom Chart Note Templates",
            "Setting up Co-signers on Your Note",
            "Sign a Chart Note",
            "Text Snippets For Your Note",
            "Chart Note Features Not Supported"
        ],
        "AI Scribe & Tooling": [
            "Additional Context Feature",
            "Complete a Visit with Air Scribe",
            "Edit with Command+K",
            "How to Apply an Air Scribe",
            "How to Set up AI Compliance",
            "Setting up AI Compliance"
        ],
        "Calendar": [
            "Getting started with the Calendar",
            "Filter the calendar view"
        ],
        "Claim Details": [
            "Submissions and Remits"
        ],
        "Patient Profiles": [
            "Getting started with Patient Profile",
            "Navigating Labs",
            "Add attachments to Patient Profile",
            "Prescribe Medications",
            "Record Allergies",
            "Record Immunizations",
            "View Patient's Appointments",
            "Profile Features Not Supported"
        ],
        "Medications": [
            "Designate Staff as Provider Agents"
        ],
        "Athelas Assistant": [
            "Getting Started with Athelas Assistant",
            "Athelas Assistant Common Functionalities",
            "Athelas Assistant Best Practices"
        ]
    },
    "Front Office Workflows": {
        "Calendar": [
            "Getting started with the Calendar",
            "Calendar start & end times",
            "Filter the calendar view",
            "Modify calendar views",
            "Viewing multiple providers",
            "Features not supported"
        ],
        "Appointments": [
            "The Insights Appointments Page",
            "Adding Prior Auth and Alerting",
            "Alternate Methods for Scheduling",
            "How to Add a Walk-In Patient",
            "How to Run an Eligibility Check",
            "How to Schedule an Appointment",
            "How to Take Payments",
            "Sending out reminders and forms",
            "Understanding Appointment Details",
            "Updating Appointment Statuses",
            "Appt. Features not supported"
        ],
        "Agents Center": [
            "Getting Started with Agents Center",
            "Components of the Dashboard",
            "Make an Outbound Call",
            "Understanding Use Cases"
        ],
        "Claim Details": [
            "Claim Details Page",
            "Other Submission Types (Secondary, Specialty etc)",
            "Encounter Timeline for Claims",
            "How to Download CMS-1500 Forms",
            "How to Resubmit a Single Claim",
            "How to Resubmit Claims in Bulk",
            "How to Send Documentation",
            "Submissions and Remits"
        ],
        "Daily Operations": [
            "How to Reconcile Your Cash Drawer"
        ],
        "Encounter Details": [
            "Encounter Details Page",
            "Insights Prior Authorization",
            "Encounter Stage and Status",
            "How to Update Insurance"
        ],
        "Faxing": [
            "Getting Started with Faxing",
            "Attach Task Follow-ups to Faxes",
            "Send and Receive a Fax",
            "Tying Faxes to Patients",
            "Tying inbound faxes to outbound faxes",
            "Faxing Features Not Supported"
        ],
        "Messaging": [
            "How to receive messages",
            "How to send messages",
            "Messages Page"
        ],
        "Patient Communications": [
            "General Patient Flows Features",
            "Text Blast Page",
            "Insurance Intake Page",
            "Functional Outcome Measurements",
            "Getting Started with Patient Portal",
            "Complete Intake Forms",
            "Navigating Patient Workflows",
            "Manage Patient Appointments",
            "Manage Payments through Patient Portal",
            "Patient Intake Automation",
            "Update Insurance Info",
            "View Home Exercise Programs"
        ],
        "Patient Demographics": [
            "Getting Started with Demographics",
            "Add/edit a Patient's Insurance",
            "Add/edit Patient Cases",
            "Add/edit Patient's Prior Authorization"
        ],
        "Patient Profiles": [
            "How to Find and Edit a Patient's Profile",
            "How to Resubmit Claim(s)"
        ],
        "Patient Responsibility": [
            "Patient Responsibility Page",
            "Charge Saved Credit Cards",
            "Manage Credit Cards",
            "Setting up a Payment Plan",
            "How to Cancel PR",
            "How to Send a Patient Payment Link",
            "How to Push to PR",
            "How to Record Payments",
            "How to Refund a Payment",
            "How to Request via Text or Email",
            "How to Set Up Miscellaneous Line Item Charges",
            "How to Take Payment for Families",
            "How to Undo a Write Off",
            "How to Write Off PR",
            "PR Overpayment Refunds and Estimated vs. Remittance PR",
            "PR Settings",
            "PR Timeline"
        ],
        "Patient Statements": [
            "Turn off Patient Texts",
            "How to Spread PR Statement Emails",
            "Manage Patient Statements",
            "Print Patient Statements",
            "Send Email Statements",
            "Send One-off Paper Statements",
            "Send Patient Statements via Email/Text"
        ],
        "Posting": [
            "How to Handle Duplicate Remittances",
            "How to Handle Partial Denials",
            "How to Post a Remittance Manually",
            "How to Use the Posting Tool Page",
            "How to Write Off a Balance"
        ],
        "Tasking": [
            "How to create tasks",
            "Sorting, Archiving, Bulk Actions"
        ],
        "Utilities": [
            "Self-service Credentialing",
            "Patient Subscriptions",
            "Process Virtual Cards",
            "Download EDI's in Bulk",
            "Bank Deposit Verification",
            "EOB Creation and Portal Checks"
        ],
        "Athelas Assistant": [
            "Getting Started With Your RCM Assistant",
            "RCM AI Prompt Library"
        ]
    },
    "Billing Workflows": {
        "Analytics": [
            "The Denials Analysis Page",
            "The Revenue Analysis Page"
        ],
        "Front Office Payments": [
            "How to Create Suggested PR Rules",
            "Self-pay Fee Schedule",
            "Target Allowed Amounts"
        ],
        "General Billing": [
            "Remittances",
            "How to Set Block PR Rules",
            "The Billing Rules Engine",
            "The Review Charges Page"
        ],
        "Reports": [
            "Building and Running Reports",
            "A/R Reports",
            "Claim Adjustments Report",
            "Collections Report",
            "Custom Collections Report",
            "Detailed Charges Report",
            "Export Claim Details",
            "Generate a Transaction Report",
            "Patient Balances Report",
            "Patient Charges Report",
            "Patient Claims One-pagers",
            "Patient Collections Report",
            "Patient Eligibility Report",
            "Posting Log Report",
            "Site Transaction Report",
            "Site Transaction Report Summary",
            "Submitted Claims Report",
            "Upcoming Patient Statements Report"
        ],
        "Athelas Assistant": [
            "Getting Started With Your RCM Assistant",
            "RCM AI Prompt Library"
        ]
    },
    "Owners & Administration": {
        "My Practice": [
            "Getting Started with Your Practice",
            "Your Athelas Invoice",
            "Manage Staff & Permissions",
            "Update Practice Information"
        ],
        "Reporting": [
            "Measuring Performance"
        ]
    }
}

def sanitize_title(title: str) -> str:
    """Sanitize title for use in filenames and folder names."""
    # Convert to lowercase
    title = title.lower()
    # Replace spaces with hyphens
    title = title.replace(" ", "-")
    # Remove special characters, keep alphanumeric and hyphens
    title = re.sub(r'[^a-z0-9\-]', '', title)
    # Remove multiple consecutive hyphens
    title = re.sub(r'-+', '-', title)
    # Remove leading/trailing hyphens
    title = title.strip('-')
    return title

def similarity(a: str, b: str) -> float:
    """Calculate similarity between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def build_mapping() -> Dict[str, Tuple[str, str, str]]:
    """Build mapping from article titles to (category, subfolder, full_path)."""
    mapping = {}
    for category, subfolders in ARCHITECTURE.items():
        for subfolder, articles in subfolders.items():
            for article in articles:
                # Handle duplicates by using full path as key
                key = f"{category}/{subfolder}/{article}"
                mapping[article] = (category, subfolder, key)
    return mapping

def find_best_match(title: str, mapping: Dict[str, Tuple[str, str, str]], threshold: float = 0.8) -> Optional[Tuple[str, str, str]]:
    """Find best matching title in mapping."""
    # Exact match first
    if title in mapping:
        return mapping[title]
    
    # Fuzzy match
    best_match = None
    best_score = 0.0
    
    for mapped_title, path_info in mapping.items():
        score = similarity(title, mapped_title)
        if score > best_score and score >= threshold:
            best_score = score
            best_match = path_info
    
    return best_match

def extract_image_urls(content: str) -> List[str]:
    """Extract image URLs from HTML content."""
    pattern = r'<img[^>]+src="([^"]+)"'
    urls = re.findall(pattern, content)
    # Filter for framerusercontent.com URLs
    return [url for url in urls if 'framerusercontent.com' in url]

def download_image(url: str, filepath: Path) -> bool:
    """Download image from URL to filepath."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False

def update_image_references(content: str, image_urls: List[str], sanitized_title: str) -> str:
    """Update image references in content to point to local paths."""
    updated_content = content
    for i, url in enumerate(image_urls, 1):
        local_path = f"/images/{sanitized_title}/{sanitized_title}-{i}.png"
        updated_content = updated_content.replace(url, local_path)
    return updated_content

def process_file(file_path: Path, mapping: Dict[str, Tuple[str, str, str]], base_dir: Path, images_dir: Path, log_file) -> bool:
    """Process a single file: extract title, match, download images, rename, move."""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            log_file.write(f"SKIP: {file_path.name} - Empty file\n")
            return False
        
        # Extract title (first line, stripped)
        title = lines[0].strip()
        content = ''.join(lines[1:]) if len(lines) > 1 else ''
        
        # Find match
        match = find_best_match(title, mapping)
        if not match:
            log_file.write(f"NO MATCH: {file_path.name} - Title: '{title}'\n")
            return False
        
        category, subfolder, full_path = match
        
        # Extract image URLs
        image_urls = extract_image_urls(content)
        
        # Sanitize title for folder/filename
        sanitized_title = sanitize_title(title)
        sanitized_subfolder = sanitize_title(subfolder)
        
        # Create destination directory
        dest_dir = base_dir / category / subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Process images
        if image_urls:
            image_folder = images_dir / sanitized_title
            image_folder.mkdir(parents=True, exist_ok=True)
            
            for i, url in enumerate(image_urls, 1):
                image_filename = f"{sanitized_title}-{i}.png"
                image_path = image_folder / image_filename
                
                if download_image(url, image_path):
                    log_file.write(f"  Downloaded: {image_filename}\n")
                else:
                    log_file.write(f"  Failed: {image_filename} from {url}\n")
            
            # Update image references in content
            content = update_image_references(content, image_urls, sanitized_title)
        
        # Create new filename
        new_filename = f"{sanitized_subfolder}-{sanitized_title}.txt"
        dest_path = dest_dir / new_filename
        
        # Write updated content
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(title + '\n\n' + content)
        
        log_file.write(f"PROCESSED: {file_path.name} -> {category}/{subfolder}/{new_filename}\n")
        return True
        
    except Exception as e:
        log_file.write(f"ERROR: {file_path.name} - {str(e)}\n")
        return False

def main():
    """Main function to organize documentation."""
    base_dir = Path(__file__).parent
    source_dir = base_dir / "DELETE-Framer-Doc"
    images_dir = base_dir / "images"
    log_path = base_dir / "organization_log.txt"
    
    # Build mapping
    print("Building title mapping...")
    mapping = build_mapping()
    print(f"Created mapping for {len(mapping)} articles")
    
    # Save mapping for reference
    mapping_file = base_dir / "file_mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
    print(f"Saved mapping to {mapping_file}")
    
    # Create images directory
    images_dir.mkdir(exist_ok=True)
    
    # Get all txt files
    txt_files = list(source_dir.glob("*.txt"))
    print(f"Found {len(txt_files)} txt files to process")
    
    # Process files
    processed = 0
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Documentation Organization Log\n")
        log_file.write("=" * 50 + "\n\n")
        
        for i, file_path in enumerate(txt_files, 1):
            print(f"Processing {i}/{len(txt_files)}: {file_path.name}")
            if process_file(file_path, mapping, base_dir, images_dir, log_file):
                processed += 1
    
    print(f"\nProcessed {processed}/{len(txt_files)} files")
    print(f"Log saved to {log_path}")
    print(f"Mapping saved to {mapping_file}")

if __name__ == "__main__":
    main()

