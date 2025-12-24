#!/usr/bin/env python3
"""
Script to generate navigation structure for Mintlify docs.json
"""

import json
from pathlib import Path
from collections import defaultdict

# Information Architecture - order matters!
ARCHITECTURE_ORDER = {
    "Provider Workflows": {
        "Chart Notes": [
            "getting-started-with-chart-notes",
            "auto-apply-kx-modifier",
            "ai-appt-summaries",
            "chart-note-clinical-types",
            "download-chart-notes-as-pdfs",
            "goals-on-the-chart-note",
            "how-to-add-measurements",
            "import-previous-medical-history",
            "navigating-flowsheets",
            "navigating-inbox-workflows",
            "navigating-the-chart-note",
            "set-up-custom-chart-note-templates",
            "setting-up-co-signers-on-your-note",
            "sign-a-chart-note",
            "text-snippets-for-your-note",
            "chart-note-features-not-supported"
        ],
        "AI Scribe & Tooling": [
            "additional-context-feature",
            "complete-a-visit-with-air-scribe",
            "edit-with-commandk",
            "how-to-apply-an-air-scribe",
            "how-to-set-up-ai-compliance",
            "setting-up-ai-compliance"
        ],
        "Calendar": [
            "getting-started-with-the-calendar",
            "filter-the-calendar-view"
        ],
        "Claim Details": [
            "submissions-and-remits"
        ],
        "Patient Profiles": [
            "getting-started-with-patient-profile",
            "navigating-labs",
            "add-attachments-to-patient-profile",
            "prescribe-medications",
            "record-allergies",
            "record-immunizations",
            "view-patients-appointments",
            "profile-features-not-supported"
        ],
        "Medications": [
            "designate-staff-as-provider-agents"
        ],
        "Athelas Assistant": [
            "getting-started-with-athelas-assistant",
            "athelas-assistant-common-functionalities",
            "athelas-assistant-best-practices"
        ]
    },
    "Front Office Workflows": {
        "Calendar": [
            "getting-started-with-the-calendar",
            "calendar-start-end-times",
            "filter-the-calendar-view",
            "modify-calendar-views",
            "viewing-multiple-providers",
            "features-not-supported"
        ],
        "Appointments": [
            "the-insights-appointments-page",
            "adding-prior-auth-and-alerting",
            "alternate-methods-for-scheduling",
            "how-to-add-a-walk-in-patient",
            "how-to-run-an-eligibility-check",
            "how-to-schedule-an-appointment",
            "how-to-take-payments",
            "sending-out-reminders-and-forms",
            "understanding-appointment-details",
            "updating-appointment-statuses",
            "appt-features-not-supported"
        ],
        "Agents Center": [
            "getting-started-with-agents-center",
            "components-of-the-dashboard",
            "make-an-outbound-call",
            "understanding-use-cases"
        ],
        "Claim Details": [
            "claim-details-page",
            "other-submission-types-secondary-specialty-etc",
            "encounter-timeline-for-claims",
            "how-to-download-cms-1500-forms",
            "how-to-resubmit-a-single-claim",
            "how-to-resubmit-claims-in-bulk",
            "how-to-send-documentation",
            "submissions-and-remits"
        ],
        "Daily Operations": [
            "how-to-reconcile-your-cash-drawer"
        ],
        "Encounter Details": [
            "encounter-details-page",
            "insights-prior-authorization",
            "encounter-stage-and-status",
            "how-to-update-insurance"
        ],
        "Faxing": [
            "getting-started-with-faxing",
            "attach-task-follow-ups-to-faxes",
            "send-and-receive-a-fax",
            "tying-faxes-to-patients",
            "tying-inbound-faxes-to-outbound-faxes",
            "faxing-features-not-supported"
        ],
        "Messaging": [
            "how-to-receive-messages",
            "how-to-send-messages",
            "messages-page"
        ],
        "Patient Communications": [
            "general-patient-flows-features",
            "text-blast-page",
            "insurance-intake-page",
            "functional-outcome-measurements",
            "getting-started-with-patient-portal",
            "complete-intake-forms",
            "navigating-patient-workflows",
            "manage-patient-appointments",
            "manage-payments-through-patient-portal",
            "patient-intake-automation",
            "update-insurance-info",
            "view-home-exercise-programs"
        ],
        "Patient Demographics": [
            "getting-started-with-demographics",
            "addedit-a-patients-insurance",
            "addedit-patient-cases",
            "addedit-patients-prior-authorization"
        ],
        "Patient Profiles": [
            "how-to-find-and-edit-a-patients-profile",
            "how-to-resubmit-claims"
        ],
        "Patient Responsibility": [
            "patient-responsibility-page",
            "charge-saved-credit-cards",
            "manage-credit-cards",
            "setting-up-a-payment-plan",
            "how-to-cancel-pr",
            "how-to-send-a-patient-payment-link",
            "how-to-push-to-pr",
            "how-to-record-payments",
            "how-to-refund-a-payment",
            "how-to-request-via-text-or-email",
            "how-to-set-up-miscellaneous-line-item-charges",
            "how-to-take-payment-for-families",
            "how-to-undo-a-write-off",
            "how-to-write-off-pr",
            "pr-overpayment-refunds-and-estimated-vs-remittance-pr",
            "pr-settings",
            "pr-timeline"
        ],
        "Patient Statements": [
            "turn-off-patient-texts",
            "how-to-spread-pr-statement-emails",
            "manage-patient-statements",
            "print-patient-statements",
            "send-email-statements",
            "send-one-off-paper-statements",
            "send-patient-statements-via-emailtext"
        ],
        "Posting": [
            "how-to-handle-duplicate-remittances",
            "how-to-handle-partial-denials",
            "how-to-post-a-remittance-manually",
            "how-to-use-the-posting-tool-page",
            "how-to-write-off-a-balance"
        ],
        "Tasking": [
            "how-to-create-tasks",
            "sorting-archiving-bulk-actions"
        ],
        "Utilities": [
            "self-service-credentialing",
            "patient-subscriptions",
            "process-virtual-cards",
            "download-edis-in-bulk",
            "bank-deposit-verification",
            "eob-creation-and-portal-checks"
        ],
        "Athelas Assistant": [
            "getting-started-with-your-rcm-assistant",
            "rcm-ai-prompt-library"
        ]
    },
    "Billing Workflows": {
        "Analytics": [
            "the-denials-analysis-page",
            "the-revenue-analysis-page"
        ],
        "Front Office Payments": [
            "how-to-create-suggested-pr-rules",
            "self-pay-fee-schedule",
            "target-allowed-amounts"
        ],
        "General Billing": [
            "remittances",
            "how-to-set-block-pr-rules",
            "the-billing-rules-engine",
            "the-review-charges-page"
        ],
        "Reports": [
            "building-and-running-reports",
            "ar-reports",
            "claim-adjustments-report",
            "collections-report",
            "custom-collections-report",
            "detailed-charges-report",
            "export-claim-details",
            "generate-a-transaction-report",
            "patient-balances-report",
            "patient-charges-report",
            "patient-claims-one-pagers",
            "patient-collections-report",
            "patient-eligibility-report",
            "posting-log-report",
            "site-transaction-report",
            "site-transaction-report-summary",
            "submitted-claims-report",
            "upcoming-patient-statements-report"
        ],
        "Athelas Assistant": [
            "getting-started-with-your-rcm-assistant",
            "rcm-ai-prompt-library"
        ]
    },
    "Owners & Administration": {
        "My Practice": [
            "getting-started-with-your-practice",
            "your-athelas-invoice",
            "manage-staff-permissions",
            "update-practice-information"
        ],
        "Reporting": [
            "measuring-performance"
        ]
    }
}

def get_file_path(category, subfolder, filename_base):
    """Convert filename to relative path."""
    # Replace spaces and special chars in category/subfolder
    category_path = category.replace(" ", " ").replace("&", "&")
    subfolder_path = subfolder.replace(" ", " ").replace("&", "&")
    return f"{category_path}/{subfolder_path}/{filename_base}"

def build_navigation_groups():
    """Build navigation groups from architecture."""
    groups = []
    
    for category, subfolders in ARCHITECTURE_ORDER.items():
        for subfolder, pages in subfolders.items():
            # Convert page names to file paths
            page_paths = []
            for page in pages:
                file_path = get_file_path(category, subfolder, page)
                page_paths.append(file_path)
            
            if page_paths:  # Only add if there are pages
                groups.append({
                    "group": subfolder,
                    "pages": page_paths
                })
    
    return groups

def main():
    """Generate navigation and update docs.json."""
    base_dir = Path(__file__).parent
    docs_json_path = base_dir / "docs.json"
    
    # Read existing docs.json
    with open(docs_json_path, 'r', encoding='utf-8') as f:
        docs = json.load(f)
    
    # Build navigation tabs
    tabs = []
    
    for category, subfolders in ARCHITECTURE_ORDER.items():
        groups = []
        for subfolder, pages in subfolders.items():
            # Convert page names to file paths
            page_paths = []
            for page in pages:
                file_path = get_file_path(category, subfolder, page)
                # Check if file exists
                file_full_path = base_dir / f"{file_path}.txt"
                if file_full_path.exists():
                    page_paths.append(file_path)
            
            if page_paths:  # Only add if there are pages
                groups.append({
                    "group": subfolder,
                    "pages": page_paths
                })
        
        if groups:  # Only add tab if it has groups
            tabs.append({
                "tab": category,
                "groups": groups
            })
    
    # Create new navigation structure
    new_navigation = {
        "tabs": tabs,
        "global": docs.get("navigation", {}).get("global", {})
    }
    
    # Update docs.json
    docs["navigation"] = new_navigation
    
    # Write updated docs.json
    with open(docs_json_path, 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
    
    total_groups = sum(len(tab["groups"]) for tab in tabs)
    print(f"Updated {docs_json_path}")
    print(f"Created {len(tabs)} tabs with {total_groups} total groups")

if __name__ == "__main__":
    main()

