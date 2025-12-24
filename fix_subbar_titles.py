#!/usr/bin/env python3
"""
Script to fix MDX subbar titles to match the reference structure.
Updates the 'title' field in frontmatter for all MDX files.
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional

# Comprehensive mapping of file paths to correct titles
# Based on the reference structure provided
TITLE_MAPPING: Dict[str, str] = {
    # Provider Workflows - Chart Notes
    "Provider Workflows/Chart Notes/getting-started-with-chart-notes.mdx": "Getting Started with Chart Notes",
    "Provider Workflows/Chart Notes/auto-apply-kx-modifier.mdx": "Auto-apply KX Modifier",
    "Provider Workflows/Chart Notes/ai-appt-summaries.mdx": "AI Appt. Summaries",
    "Provider Workflows/Chart Notes/chart-note-clinical-types.mdx": "Chart Note Clinical Types",
    "Provider Workflows/Chart Notes/download-chart-notes-as-pdfs.mdx": "Download Chart Notes as PDFs",
    "Provider Workflows/Chart Notes/goals-on-the-chart-note.mdx": "Goals on the chart note",
    "Provider Workflows/Chart Notes/how-to-add-measurements.mdx": "How to add Measurements",
    "Provider Workflows/Chart Notes/import-previous-medical-history.mdx": "Import Previous Medical History",
    "Provider Workflows/Chart Notes/navigating-flowsheets.mdx": "Navigating Flowsheets",
    "Provider Workflows/Chart Notes/navigating-inbox-workflows.mdx": "Navigating Inbox Workflows",
    "Provider Workflows/Chart Notes/navigating-the-chart-note.mdx": "Navigating the Chart Note",
    "Provider Workflows/Chart Notes/set-up-custom-chart-note-templates.mdx": "Set up Custom Chart Note Templates",
    "Provider Workflows/Chart Notes/setting-up-co-signers-on-your-note.mdx": "Setting up Co-signers on Your Note",
    "Provider Workflows/Chart Notes/sign-a-chart-note.mdx": "Sign a Chart Note",
    "Provider Workflows/Chart Notes/text-snippets-for-your-note.mdx": "Text Snippets For Your Note",
    "Provider Workflows/Chart Notes/chart-note-features-not-supported.mdx": "Chart Note Features Not Supported",
    
    # Provider Workflows - AI Scribe & Tooling
    "Provider Workflows/AI Scribe & Tooling/additional-context-feature.mdx": "Additional Context Feature",
    "Provider Workflows/AI Scribe & Tooling/complete-a-visit-with-air-scribe.mdx": "Complete a Visit with Air Scribe",
    "Provider Workflows/AI Scribe & Tooling/edit-with-commandk.mdx": "Edit with Command+K",
    "Provider Workflows/AI Scribe & Tooling/how-to-apply-an-air-scribe.mdx": "How to Apply an Air Scribe",
    "Provider Workflows/AI Scribe & Tooling/how-to-set-up-ai-compliance.mdx": "How to Set up AI Compliance",
    "Provider Workflows/AI Scribe & Tooling/setting-up-ai-compliance.mdx": "Setting up AI Compliance",
    
    # Provider Workflows - Calendar
    "Provider Workflows/Calendar/getting-started-with-the-calendar.mdx": "Getting started with the Calendar",
    "Provider Workflows/Calendar/filter-the-calendar-view.mdx": "Filter the calendar view",
    
    # Provider Workflows - Claim Details
    "Provider Workflows/Claim Details/submissions-and-remits.mdx": "Submissions and Remits",
    
    # Provider Workflows - Patient Profiles
    "Provider Workflows/Patient Profiles/getting-started-with-patient-profile.mdx": "Getting started with Patient Profile",
    "Provider Workflows/Patient Profiles/navigating-labs.mdx": "Navigating Labs",
    "Provider Workflows/Patient Profiles/add-attachments-to-patient-profile.mdx": "Add attachments to Patient Profile",
    "Provider Workflows/Patient Profiles/prescribe-medications.mdx": "Prescribe Medications",
    "Provider Workflows/Patient Profiles/record-allergies.mdx": "Record Allergies",
    "Provider Workflows/Patient Profiles/record-immunizations.mdx": "Record Immunizations",
    "Provider Workflows/Patient Profiles/view-patients-appointments.mdx": "View Patient's Appointments",
    "Provider Workflows/Patient Profiles/profile-features-not-supported.mdx": "Profile Features Not Supported",
    
    # Provider Workflows - Medications
    "Provider Workflows/Medications/designate-staff-as-provider-agents.mdx": "Designate Staff as Provider Agents",
    
    # Provider Workflows - Athelas Assistant
    "Provider Workflows/Athelas Assistant/getting-started-with-athelas-assistant.mdx": "Getting Started with Athelas Assistant",
    "Provider Workflows/Athelas Assistant/athelas-assistant-common-functionalities.mdx": "Athelas Assistant Common Functionalities",
    "Provider Workflows/Athelas Assistant/athelas-assistant-best-practices.mdx": "Athelas Assistant Best Practices",
    
    # Front Office Workflows - Calendar
    "Front Office Workflows/Calendar/getting-started-with-the-calendar.mdx": "Getting started with the Calendar",
    "Front Office Workflows/Calendar/calendar-start-end-times.mdx": "Calendar start & end times",
    "Front Office Workflows/Calendar/filter-the-calendar-view.mdx": "Filter the calendar view",
    "Front Office Workflows/Calendar/modify-calendar-views.mdx": "Modify calendar views",
    "Front Office Workflows/Calendar/viewing-multiple-providers.mdx": "Viewing multiple providers",
    "Front Office Workflows/Calendar/features-not-supported.mdx": "Features not supported",
    
    # Front Office Workflows - Appointments
    "Front Office Workflows/Appointments/the-insights-appointments-page.mdx": "The Insights Appointments Page",
    "Front Office Workflows/Appointments/adding-prior-auth-and-alerting.mdx": "Adding Prior Auth and Alerting",
    "Front Office Workflows/Appointments/alternate-methods-for-scheduling.mdx": "Alternate Methods for Scheduling",
    "Front Office Workflows/Appointments/how-to-add-a-walk-in-patient.mdx": "How to Add a Walk-In Patient",
    "Front Office Workflows/Appointments/how-to-run-an-eligibility-check.mdx": "How to Run an Eligibility Check",
    "Front Office Workflows/Appointments/how-to-schedule-an-appointment.mdx": "How to Schedule an Appointment",
    "Front Office Workflows/Appointments/how-to-take-payments.mdx": "How to Take Payments",
    "Front Office Workflows/Appointments/sending-out-reminders-and-forms.mdx": "Sending out reminders and forms",
    "Front Office Workflows/Appointments/understanding-appointment-details.mdx": "Understanding Appointment Details",
    "Front Office Workflows/Appointments/updating-appointment-statuses.mdx": "Updating Appointment Statuses",
    "Front Office Workflows/Appointments/appt-features-not-supported.mdx": "Appt. Features not supported",
    
    # Front Office Workflows - Agents Center
    "Front Office Workflows/Agents Center/getting-started-with-agents-center.mdx": "Getting Started with Agents Center",
    "Front Office Workflows/Agents Center/components-of-the-dashboard.mdx": "Components of the Dashboard",
    "Front Office Workflows/Agents Center/make-an-outbound-call.mdx": "Make an Outbound Call",
    "Front Office Workflows/Agents Center/understanding-use-cases.mdx": "Understanding Use Cases",
    
    # Front Office Workflows - Claim Details
    "Front Office Workflows/Claim Details/claim-details-page.mdx": "Claim Details Page",
    "Front Office Workflows/Claim Details/other-submission-types-secondary-specialty-etc.mdx": "Other Submission Types (Secondary, Specialty etc)",
    "Front Office Workflows/Claim Details/encounter-timeline-for-claims.mdx": "Encounter Timeline for Claims",
    "Front Office Workflows/Claim Details/how-to-download-cms-1500-forms.mdx": "How to Download CMS-1500 Forms",
    "Front Office Workflows/Claim Details/how-to-resubmit-a-single-claim.mdx": "How to Resubmit a Single Claim",
    "Front Office Workflows/Claim Details/how-to-resubmit-claims-in-bulk.mdx": "How to Resubmit Claims in Bulk",
    "Front Office Workflows/Claim Details/how-to-send-documentation.mdx": "How to Send Documentation",
    "Front Office Workflows/Claim Details/submissions-and-remits.mdx": "Submissions and Remits",
    
    # Front Office Workflows - Daily Operations
    "Front Office Workflows/Daily Operations/how-to-reconcile-your-cash-drawer.mdx": "How to Reconcile Your Cash Drawer",
    
    # Front Office Workflows - Encounter Details
    "Front Office Workflows/Encounter Details/encounter-details-page.mdx": "Encounter Details Page",
    "Front Office Workflows/Encounter Details/insights-prior-authorization.mdx": "Insights Prior Authorization",
    "Front Office Workflows/Encounter Details/encounter-stage-and-status.mdx": "Encounter Stage and Status",
    "Front Office Workflows/Encounter Details/how-to-update-insurance.mdx": "How to Update Insurance",
    
    # Front Office Workflows - Faxing
    "Front Office Workflows/Faxing/getting-started-with-faxing.mdx": "Getting Started with Faxing",
    "Front Office Workflows/Faxing/attach-task-follow-ups-to-faxes.mdx": "Attach Task Follow-ups to Faxes",
    "Front Office Workflows/Faxing/send-and-receive-a-fax.mdx": "Send and Receive a Fax",
    "Front Office Workflows/Faxing/tying-faxes-to-patients.mdx": "Tying Faxes to Patients",
    "Front Office Workflows/Faxing/tying-inbound-faxes-to-outbound-faxes.mdx": "Tying inbound faxes to outbound faxes",
    "Front Office Workflows/Faxing/faxing-features-not-supported.mdx": "Faxing Features Not Supported",
    
    # Front Office Workflows - Messaging
    "Front Office Workflows/Messaging/how-to-receive-messages.mdx": "How to receive messages",
    "Front Office Workflows/Messaging/how-to-send-messages.mdx": "How to send messages",
    "Front Office Workflows/Messaging/messages-page.mdx": "Messages Page",
    
    # Front Office Workflows - Patient Communications
    "Front Office Workflows/Patient Communications/general-patient-flows-features.mdx": "General Patient Flows Features",
    "Front Office Workflows/Patient Communications/text-blast-page.mdx": "Text Blast Page",
    "Front Office Workflows/Patient Communications/insurance-intake-page.mdx": "Insurance Intake Page",
    "Front Office Workflows/Patient Communications/functional-outcome-measurements.mdx": "Functional Outcome Measurements",
    "Front Office Workflows/Patient Communications/getting-started-with-patient-portal.mdx": "Getting Started with Patient Portal",
    "Front Office Workflows/Patient Communications/complete-intake-forms.mdx": "Complete Intake Forms",
    "Front Office Workflows/Patient Communications/navigating-patient-workflows.mdx": "Navigating Patient Workflows",
    "Front Office Workflows/Patient Communications/manage-patient-appointments.mdx": "Manage Patient Appointments",
    "Front Office Workflows/Patient Communications/manage-payments-through-patient-portal.mdx": "Manage Payments through Patient Portal",
    "Front Office Workflows/Patient Communications/patient-intake-automation.mdx": "Patient Intake Automation",
    "Front Office Workflows/Patient Communications/update-insurance-info.mdx": "Update Insurance Info",
    "Front Office Workflows/Patient Communications/view-home-exercise-programs.mdx": "View Home Exercise Programs",
    
    # Front Office Workflows - Patient Demographics
    "Front Office Workflows/Patient Demographics/getting-started-with-demographics.mdx": "Getting Started with Demographics",
    "Front Office Workflows/Patient Demographics/addedit-a-patients-insurance.mdx": "Add/edit a Patient's Insurance",
    "Front Office Workflows/Patient Demographics/addedit-patient-cases.mdx": "Add/edit Patient Cases",
    "Front Office Workflows/Patient Demographics/addedit-patients-prior-authorization.mdx": "Add/edit Patient's Prior Authorization",
    
    # Front Office Workflows - Patient Profiles
    "Front Office Workflows/Patient Profiles/how-to-find-and-edit-a-patients-profile.mdx": "How to Find and Edit a Patient's Profile",
    "Front Office Workflows/Patient Profiles/how-to-resubmit-claims.mdx": "How to Resubmit Claim(s)",
    
    # Front Office Workflows - Patient Responsibility
    "Front Office Workflows/Patient Responsibility/patient-responsibility-page.mdx": "Patient Responsibility Page",
    "Front Office Workflows/Patient Responsibility/charge-saved-credit-cards.mdx": "Charge Saved Credit Cards",
    "Front Office Workflows/Patient Responsibility/manage-credit-cards.mdx": "Manage Credit Cards",
    "Front Office Workflows/Patient Responsibility/setting-up-a-payment-plan.mdx": "Setting up a Payment Plan",
    "Front Office Workflows/Patient Responsibility/how-to-cancel-pr.mdx": "How to Cancel PR",
    "Front Office Workflows/Patient Responsibility/how-to-send-a-patient-payment-link.mdx": "How to Send a Patient Payment Link",
    "Front Office Workflows/Patient Responsibility/how-to-push-to-pr.mdx": "How to Push to PR",
    "Front Office Workflows/Patient Responsibility/how-to-record-payments.mdx": "How to Record Payments",
    "Front Office Workflows/Patient Responsibility/how-to-refund-a-payment.mdx": "How to Refund a Payment",
    "Front Office Workflows/Patient Responsibility/how-to-request-via-text-or-email.mdx": "How to Request via Text or Email",
    "Front Office Workflows/Patient Responsibility/how-to-set-up-miscellaneous-line-item-charges.mdx": "How to Set Up Miscellaneous Line Item Charges",
    "Front Office Workflows/Patient Responsibility/how-to-take-payment-for-families.mdx": "How to Take Payment for Families",
    "Front Office Workflows/Patient Responsibility/how-to-undo-a-write-off.mdx": "How to Undo a Write Off",
    "Front Office Workflows/Patient Responsibility/how-to-write-off-pr.mdx": "How to Write Off PR",
    "Front Office Workflows/Patient Responsibility/pr-overpayment-refunds-and-estimated-vs-remittance-pr.mdx": "PR Overpayment Refunds and Estimated vs. Remittance PR",
    "Front Office Workflows/Patient Responsibility/pr-settings.mdx": "PR Settings",
    "Front Office Workflows/Patient Responsibility/pr-timeline.mdx": "PR Timeline",
    
    # Front Office Workflows - Patient Statements
    "Front Office Workflows/Patient Statements/turn-off-patient-texts.mdx": "Turn off Patient Texts",
    "Front Office Workflows/Patient Statements/how-to-spread-pr-statement-emails.mdx": "How to Spread PR Statement Emails",
    "Front Office Workflows/Patient Statements/manage-patient-statements.mdx": "Manage Patient Statements",
    "Front Office Workflows/Patient Statements/print-patient-statements.mdx": "Print Patient Statements",
    "Front Office Workflows/Patient Statements/send-email-statements.mdx": "Send Email Statements",
    "Front Office Workflows/Patient Statements/send-one-off-paper-statements.mdx": "Send One-off Paper Statements",
    "Front Office Workflows/Patient Statements/send-patient-statements-via-emailtext.mdx": "Send Patient Statements via Email/Text",
    
    # Front Office Workflows - Posting
    "Front Office Workflows/Posting/how-to-handle-duplicate-remittances.mdx": "How to Handle Duplicate Remittances",
    "Front Office Workflows/Posting/how-to-handle-partial-denials.mdx": "How to Handle Partial Denials",
    "Front Office Workflows/Posting/how-to-post-a-remittance-manually.mdx": "How to Post a Remittance Manually",
    "Front Office Workflows/Posting/how-to-use-the-posting-tool-page.mdx": "How to Use the Posting Tool Page",
    "Front Office Workflows/Posting/how-to-write-off-a-balance.mdx": "How to Write Off a Balance",
    
    # Front Office Workflows - Tasking
    "Front Office Workflows/Tasking/how-to-create-tasks.mdx": "How to create tasks",
    "Front Office Workflows/Tasking/sorting-archiving-bulk-actions.mdx": "Sorting, Archiving, Bulk Actions",
    
    # Front Office Workflows - Utilities
    "Front Office Workflows/Utilities/self-service-credentialing.mdx": "Self-service Credentialing",
    "Front Office Workflows/Utilities/patient-subscriptions.mdx": "Patient Subscriptions",
    "Front Office Workflows/Utilities/process-virtual-cards.mdx": "Process Virtual Cards",
    "Front Office Workflows/Utilities/download-edis-in-bulk.mdx": "Download EDI's in Bulk",
    "Front Office Workflows/Utilities/bank-deposit-verification.mdx": "Bank Deposit Verification",
    "Front Office Workflows/Utilities/eob-creation-and-portal-checks.mdx": "EOB Creation and Portal Checks",
    
    # Front Office Workflows - Athelas Assistant
    "Front Office Workflows/Athelas Assistant/getting-started-with-your-rcm-assistant.mdx": "Getting Started With Your RCM Assistant",
    "Front Office Workflows/Athelas Assistant/rcm-ai-prompt-library.mdx": "RCM AI Prompt Library",
    
    # Billing Workflows - Analytics
    "Billing Workflows/Analytics/the-denials-analysis-page.mdx": "The Denials Analysis Page",
    "Billing Workflows/Analytics/the-revenue-analysis-page.mdx": "The Revenue Analysis Page",
    
    # Billing Workflows - Front Office Payments
    "Billing Workflows/Front Office Payments/how-to-create-suggested-pr-rules.mdx": "How to Create Suggested PR Rules",
    "Billing Workflows/Front Office Payments/self-pay-fee-schedule.mdx": "Self-pay Fee Schedule",
    "Billing Workflows/Front Office Payments/target-allowed-amounts.mdx": "Target Allowed Amounts",
    
    # Billing Workflows - General Billing
    "Billing Workflows/General Billing/remittances.mdx": "Remittances",
    "Billing Workflows/General Billing/how-to-set-block-pr-rules.mdx": "How to Set Block PR Rules",
    "Billing Workflows/General Billing/the-billing-rules-engine.mdx": "The Billing Rules Engine",
    "Billing Workflows/General Billing/the-review-charges-page.mdx": "The Review Charges Page",
    
    # Billing Workflows - Reports
    "Billing Workflows/Reports/building-and-running-reports.mdx": "Building and Running Reports",
    "Billing Workflows/Reports/ar-reports.mdx": "A/R Reports",
    "Billing Workflows/Reports/claim-adjustments-report.mdx": "Claim Adjustments Report",
    "Billing Workflows/Reports/collections-report.mdx": "Collections Report",
    "Billing Workflows/Reports/custom-collections-report.mdx": "Custom Collections Report",
    "Billing Workflows/Reports/detailed-charges-report.mdx": "Detailed Charges Report",
    "Billing Workflows/Reports/export-claim-details.mdx": "Export Claim Details",
    "Billing Workflows/Reports/generate-a-transaction-report.mdx": "Generate a Transaction Report",
    "Billing Workflows/Reports/patient-balances-report.mdx": "Patient Balances Report",
    "Billing Workflows/Reports/patient-charges-report.mdx": "Patient Charges Report",
    "Billing Workflows/Reports/patient-claims-one-pagers.mdx": "Patient Claims One-pagers",
    "Billing Workflows/Reports/patient-collections-report.mdx": "Patient Collections Report",
    "Billing Workflows/Reports/patient-eligibility-report.mdx": "Patient Eligibility Report",
    "Billing Workflows/Reports/posting-log-report.mdx": "Posting Log Report",
    "Billing Workflows/Reports/site-transaction-report.mdx": "Site Transaction Report",
    "Billing Workflows/Reports/site-transaction-report-summary.mdx": "Site Transaction Report Summary",
    "Billing Workflows/Reports/submitted-claims-report.mdx": "Submitted Claims Report",
    "Billing Workflows/Reports/upcoming-patient-statements-report.mdx": "Upcoming Patient Statements Report",
    
    # Billing Workflows - Athelas Assistant
    "Billing Workflows/Athelas Assistant/getting-started-with-your-rcm-assistant.mdx": "Getting Started With Your RCM Assistant",
    "Billing Workflows/Athelas Assistant/rcm-ai-prompt-library.mdx": "RCM AI Prompt Library",
    
    # Owners & Administration - My Practice
    "Owners & Administration/My Practice/getting-started-with-your-practice.mdx": "Getting Started with Your Practice",
    "Owners & Administration/My Practice/your-athelas-invoice.mdx": "Your Athelas Invoice",
    "Owners & Administration/My Practice/manage-staff-permissions.mdx": "Manage Staff & Permissions",
    "Owners & Administration/My Practice/update-practice-information.mdx": "Update Practice Information",
    
    # Owners & Administration - Reporting
    "Owners & Administration/Reporting/measuring-performance.mdx": "Measuring Performance",
}


def extract_frontmatter_title(content: str) -> Optional[str]:
    """Extract the title from frontmatter."""
    # Match frontmatter with title field
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return None
    
    frontmatter = frontmatter_match.group(1)
    title_match = re.search(r'^title:\s*[\'"](.*?)[\'"]', frontmatter, re.MULTILINE)
    if title_match:
        return title_match.group(1)
    return None


def update_frontmatter_title(content: str, new_title: str) -> str:
    """Update the title in frontmatter, preserving formatting."""
    # Match the entire frontmatter block
    def replace_title(match):
        frontmatter = match.group(1)
        # Replace the title line, handling both single and double quotes
        updated = re.sub(
            r'^title:\s*[\'"](.*?)[\'"]',
            f"title: '{new_title}'",
            frontmatter,
            flags=re.MULTILINE
        )
        return f"---\n{updated}\n---"
    
    # Replace frontmatter with updated title
    result = re.sub(
        r'^---\s*\n(.*?)\n---',
        replace_title,
        content,
        flags=re.DOTALL
    )
    
    return result


def process_mdx_file(file_path: Path, correct_title: str) -> bool:
    """Process a single MDX file and update its title."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        current_title = extract_frontmatter_title(content)
        
        if current_title == correct_title:
            print(f"✓ {file_path.name}: Already correct ('{correct_title}')")
            return False
        
        if current_title is None:
            print(f"⚠ {file_path.name}: No frontmatter title found, skipping")
            return False
        
        # Update the title
        updated_content = update_frontmatter_title(content, correct_title)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✓ {file_path.name}: '{current_title}' → '{correct_title}'")
        return True
        
    except Exception as e:
        print(f"✗ {file_path.name}: Error - {e}")
        return False


def main():
    """Main function to process all MDX files."""
    base_dir = Path(__file__).parent
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    print("Fixing MDX subbar titles...\n")
    
    # Process all files in the mapping
    for relative_path, correct_title in TITLE_MAPPING.items():
        file_path = base_dir / relative_path
        
        if not file_path.exists():
            print(f"⚠ {relative_path}: File not found, skipping")
            skipped_count += 1
            continue
        
        if process_mdx_file(file_path, correct_title):
            updated_count += 1
        else:
            skipped_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"  Errors: {error_count} files")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

