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
            "chart-notes-getting-started-with-chart-notes",
            "chart-notes-auto-apply-kx-modifier",
            "chart-notes-ai-appt-summaries",
            "chart-notes-chart-note-clinical-types",
            "chart-notes-download-chart-notes-as-pdfs",
            "chart-notes-goals-on-the-chart-note",
            "chart-notes-how-to-add-measurements",
            "chart-notes-import-previous-medical-history",
            "chart-notes-navigating-flowsheets",
            "chart-notes-navigating-inbox-workflows",
            "chart-notes-navigating-the-chart-note",
            "chart-notes-set-up-custom-chart-note-templates",
            "chart-notes-setting-up-co-signers-on-your-note",
            "chart-notes-sign-a-chart-note",
            "chart-notes-text-snippets-for-your-note",
            "chart-notes-chart-note-features-not-supported"
        ],
        "AI Scribe & Tooling": [
            "ai-scribe-tooling-additional-context-feature",
            "ai-scribe-tooling-complete-a-visit-with-air-scribe",
            "ai-scribe-tooling-edit-with-commandk",
            "ai-scribe-tooling-how-to-apply-an-air-scribe",
            "ai-scribe-tooling-how-to-set-up-ai-compliance",
            "ai-scribe-tooling-setting-up-ai-compliance"
        ],
        "Calendar": [
            "calendar-getting-started-with-the-calendar",
            "calendar-filter-the-calendar-view"
        ],
        "Claim Details": [
            "claim-details-submissions-and-remits"
        ],
        "Patient Profiles": [
            "patient-profiles-getting-started-with-patient-profile",
            "patient-profiles-navigating-labs",
            "patient-profiles-add-attachments-to-patient-profile",
            "patient-profiles-prescribe-medications",
            "patient-profiles-record-allergies",
            "patient-profiles-record-immunizations",
            "patient-profiles-view-patients-appointments",
            "patient-profiles-profile-features-not-supported"
        ],
        "Medications": [
            "medications-designate-staff-as-provider-agents"
        ],
        "Athelas Assistant": [
            "athelas-assistant-getting-started-with-athelas-assistant",
            "athelas-assistant-athelas-assistant-common-functionalities",
            "athelas-assistant-athelas-assistant-best-practices"
        ]
    },
    "Front Office Workflows": {
        "Calendar": [
            "calendar-getting-started-with-the-calendar",
            "calendar-calendar-start-end-times",
            "calendar-filter-the-calendar-view",
            "calendar-modify-calendar-views",
            "calendar-viewing-multiple-providers",
            "calendar-features-not-supported"
        ],
        "Appointments": [
            "appointments-the-insights-appointments-page",
            "appointments-adding-prior-auth-and-alerting",
            "appointments-alternate-methods-for-scheduling",
            "appointments-how-to-add-a-walk-in-patient",
            "appointments-how-to-run-an-eligibility-check",
            "appointments-how-to-schedule-an-appointment",
            "appointments-how-to-take-payments",
            "appointments-sending-out-reminders-and-forms",
            "appointments-understanding-appointment-details",
            "appointments-updating-appointment-statuses",
            "appointments-appt-features-not-supported"
        ],
        "Agents Center": [
            "agents-center-getting-started-with-agents-center",
            "agents-center-components-of-the-dashboard",
            "agents-center-make-an-outbound-call",
            "agents-center-understanding-use-cases"
        ],
        "Claim Details": [
            "claim-details-claim-details-page",
            "claim-details-other-submission-types-secondary-specialty-etc",
            "claim-details-encounter-timeline-for-claims",
            "claim-details-how-to-download-cms-1500-forms",
            "claim-details-how-to-resubmit-a-single-claim",
            "claim-details-how-to-resubmit-claims-in-bulk",
            "claim-details-how-to-send-documentation",
            "claim-details-submissions-and-remits"
        ],
        "Daily Operations": [
            "daily-operations-how-to-reconcile-your-cash-drawer"
        ],
        "Encounter Details": [
            "encounter-details-encounter-details-page",
            "encounter-details-insights-prior-authorization",
            "encounter-details-encounter-stage-and-status",
            "encounter-details-how-to-update-insurance"
        ],
        "Faxing": [
            "faxing-getting-started-with-faxing",
            "faxing-attach-task-follow-ups-to-faxes",
            "faxing-send-and-receive-a-fax",
            "faxing-tying-faxes-to-patients",
            "faxing-tying-inbound-faxes-to-outbound-faxes",
            "faxing-faxing-features-not-supported"
        ],
        "Messaging": [
            "messaging-how-to-receive-messages",
            "messaging-how-to-send-messages",
            "messaging-messages-page"
        ],
        "Patient Communications": [
            "patient-communications-general-patient-flows-features",
            "patient-communications-text-blast-page",
            "patient-communications-insurance-intake-page",
            "patient-communications-functional-outcome-measurements",
            "patient-communications-getting-started-with-patient-portal",
            "patient-communications-complete-intake-forms",
            "patient-communications-navigating-patient-workflows",
            "patient-communications-manage-patient-appointments",
            "patient-communications-manage-payments-through-patient-portal",
            "patient-communications-patient-intake-automation",
            "patient-communications-update-insurance-info",
            "patient-communications-view-home-exercise-programs"
        ],
        "Patient Demographics": [
            "patient-demographics-getting-started-with-demographics",
            "patient-demographics-addedit-a-patients-insurance",
            "patient-demographics-addedit-patient-cases",
            "patient-demographics-addedit-patients-prior-authorization"
        ],
        "Patient Profiles": [
            "patient-profiles-how-to-find-and-edit-a-patients-profile",
            "patient-profiles-how-to-resubmit-claims"
        ],
        "Patient Responsibility": [
            "patient-responsibility-patient-responsibility-page",
            "patient-responsibility-charge-saved-credit-cards",
            "patient-responsibility-manage-credit-cards",
            "patient-responsibility-setting-up-a-payment-plan",
            "patient-responsibility-how-to-cancel-pr",
            "patient-responsibility-how-to-send-a-patient-payment-link",
            "patient-responsibility-how-to-push-to-pr",
            "patient-responsibility-how-to-record-payments",
            "patient-responsibility-how-to-refund-a-payment",
            "patient-responsibility-how-to-request-via-text-or-email",
            "patient-responsibility-how-to-set-up-miscellaneous-line-item-charges",
            "patient-responsibility-how-to-take-payment-for-families",
            "patient-responsibility-how-to-undo-a-write-off",
            "patient-responsibility-how-to-write-off-pr",
            "patient-responsibility-pr-overpayment-refunds-and-estimated-vs-remittance-pr",
            "patient-responsibility-pr-settings",
            "patient-responsibility-pr-timeline"
        ],
        "Patient Statements": [
            "patient-statements-turn-off-patient-texts",
            "patient-statements-how-to-spread-pr-statement-emails",
            "patient-statements-manage-patient-statements",
            "patient-statements-print-patient-statements",
            "patient-statements-send-email-statements",
            "patient-statements-send-one-off-paper-statements",
            "patient-statements-send-patient-statements-via-emailtext"
        ],
        "Posting": [
            "posting-how-to-handle-duplicate-remittances",
            "posting-how-to-handle-partial-denials",
            "posting-how-to-post-a-remittance-manually",
            "posting-how-to-use-the-posting-tool-page",
            "posting-how-to-write-off-a-balance"
        ],
        "Tasking": [
            "tasking-how-to-create-tasks",
            "tasking-sorting-archiving-bulk-actions"
        ],
        "Utilities": [
            "utilities-self-service-credentialing",
            "utilities-patient-subscriptions",
            "utilities-process-virtual-cards",
            "utilities-download-edis-in-bulk",
            "utilities-bank-deposit-verification",
            "utilities-eob-creation-and-portal-checks"
        ],
        "Athelas Assistant": [
            "athelas-assistant-getting-started-with-your-rcm-assistant",
            "athelas-assistant-rcm-ai-prompt-library"
        ]
    },
    "Billing Workflows": {
        "Analytics": [
            "analytics-the-denials-analysis-page",
            "analytics-the-revenue-analysis-page"
        ],
        "Front Office Payments": [
            "front-office-payments-how-to-create-suggested-pr-rules",
            "front-office-payments-self-pay-fee-schedule",
            "front-office-payments-target-allowed-amounts"
        ],
        "General Billing": [
            "general-billing-remittances",
            "general-billing-how-to-set-block-pr-rules",
            "general-billing-the-billing-rules-engine",
            "general-billing-the-review-charges-page"
        ],
        "Reports": [
            "reports-building-and-running-reports",
            "reports-ar-reports",
            "reports-claim-adjustments-report",
            "reports-collections-report",
            "reports-custom-collections-report",
            "reports-detailed-charges-report",
            "reports-export-claim-details",
            "reports-generate-a-transaction-report",
            "reports-patient-balances-report",
            "reports-patient-charges-report",
            "reports-patient-claims-one-pagers",
            "reports-patient-collections-report",
            "reports-patient-eligibility-report",
            "reports-posting-log-report",
            "reports-site-transaction-report",
            "reports-site-transaction-report-summary",
            "reports-submitted-claims-report",
            "reports-upcoming-patient-statements-report"
        ],
        "Athelas Assistant": [
            "athelas-assistant-getting-started-with-your-rcm-assistant",
            "athelas-assistant-rcm-ai-prompt-library"
        ]
    },
    "Owners & Administration": {
        "My Practice": [
            "my-practice-getting-started-with-your-practice",
            "my-practice-your-athelas-invoice",
            "my-practice-manage-staff-permissions",
            "my-practice-update-practice-information"
        ],
        "Reporting": [
            "reporting-measuring-performance"
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

