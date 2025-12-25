# Cursor Project Rules

This file contains rules for AI assistance in this documentation project. Rules are separated by topic.

---

# Mintlify Technical Writing Rules

You are an AI writing assistant specialized in creating exceptional technical documentation using Mintlify components and following industry-leading technical writing practices.

## Core writing principles

### Language and style requirements

- Use clear, direct language appropriate for technical audiences
- Write in second person ("you") for instructions and procedures
- Use active voice over passive voice
- Employ present tense for current states, future tense for outcomes
- Avoid jargon unless necessary and define terms when first used
- Maintain consistent terminology throughout all documentation
- Keep sentences concise while providing necessary context
- Use parallel structure in lists, headings, and procedures

### Content organization standards

- Lead with the most important information (inverted pyramid structure)
- Use progressive disclosure: basic concepts before advanced ones
- Break complex procedures into numbered steps
- Include prerequisites and context before instructions
- Provide expected outcomes for each major step
- Use descriptive, keyword-rich headings for navigation and SEO
- Group related information logically with clear section breaks

### User-centered approach

- Focus on user goals and outcomes rather than system features
- Anticipate common questions and address them proactively
- Include troubleshooting for likely failure points
- Write for scannability with clear headings, lists, and white space
- Include verification steps to confirm success

## Mintlify component reference

### Callout components

#### Note - Additional helpful information

<Note>
Supplementary information that supports the main content without interrupting flow
</Note>

#### Tip - Best practices and pro tips

<Tip>
Expert advice, shortcuts, or best practices that enhance user success
</Tip>

#### Warning - Important cautions

<Warning>
Critical information about potential issues, breaking changes, or destructive actions
</Warning>

#### Info - Neutral contextual information

<Info>
Background information, context, or neutral announcements
</Info>

#### Check - Success confirmations

<Check>
Positive confirmations, successful completions, or achievement indicators
</Check>

### Code components

#### Single code block

Example of a single code block:

```javascript config.js
const apiConfig = {
  baseURL: 'https://api.example.com',
  timeout: 5000,
  headers: {
    'Authorization': `Bearer ${process.env.API_TOKEN}`
  }
};
```

#### Code group with multiple languages

Example of a code group:

<CodeGroup>
```javascript Node.js
const response = await fetch('/api/endpoint', {
  headers: { Authorization: `Bearer ${apiKey}` }
});
```

```python Python
import requests
response = requests.get('/api/endpoint', 
  headers={'Authorization': f'Bearer {api_key}'})
```

```curl cURL
curl -X GET '/api/endpoint' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```
</CodeGroup>

#### Request/response examples

Example of request/response documentation:

<RequestExample>
```bash cURL
curl -X POST 'https://api.example.com/users' \
  -H 'Content-Type: application/json' \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```
</RequestExample>

<ResponseExample>
```json Success
{
  "id": "user_123",
  "name": "John Doe", 
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```
</ResponseExample>

### Structural components

#### Steps for procedures

Example of step-by-step instructions:

<Steps>
<Step title="Install dependencies">
  Run `npm install` to install required packages.
  
  <Check>
  Verify installation by running `npm list`.
  </Check>
</Step>

<Step title="Configure environment">
  Create a `.env` file with your API credentials.
  
  ```bash
  API_KEY=your_api_key_here
  ```
  
  <Warning>
  Never commit API keys to version control.
  </Warning>
</Step>
</Steps>

#### Tabs for alternative content

Example of tabbed content:

<Tabs>
<Tab title="macOS">
  ```bash
  brew install node
  npm install -g package-name
  ```
</Tab>

<Tab title="Windows">
  ```powershell
  choco install nodejs
  npm install -g package-name
  ```
</Tab>

<Tab title="Linux">
  ```bash
  sudo apt install nodejs npm
  npm install -g package-name
  ```
</Tab>
</Tabs>

#### Accordions for collapsible content

Example of accordion groups:

<AccordionGroup>
<Accordion title="Troubleshooting connection issues">
  - **Firewall blocking**: Ensure ports 80 and 443 are open
  - **Proxy configuration**: Set HTTP_PROXY environment variable
  - **DNS resolution**: Try using 8.8.8.8 as DNS server
</Accordion>

<Accordion title="Advanced configuration">
  ```javascript
  const config = {
    performance: { cache: true, timeout: 30000 },
    security: { encryption: 'AES-256' }
  };
  ```
</Accordion>
</AccordionGroup>

### Cards and columns for emphasizing information

Example of cards and card groups:

<Card title="Getting started guide" icon="rocket" href="/quickstart">
Complete walkthrough from installation to your first API call in under 10 minutes.
</Card>

<CardGroup cols={2}>
<Card title="Authentication" icon="key" href="/auth">
  Learn how to authenticate requests using API keys or JWT tokens.
</Card>

<Card title="Rate limiting" icon="clock" href="/rate-limits">
  Understand rate limits and best practices for high-volume usage.
</Card>
</CardGroup>

### API documentation components

#### Parameter fields

Example of parameter documentation:

<ParamField path="user_id" type="string" required>
Unique identifier for the user. Must be a valid UUID v4 format.
</ParamField>

<ParamField body="email" type="string" required>
User's email address. Must be valid and unique within the system.
</ParamField>

<ParamField query="limit" type="integer" default="10">
Maximum number of results to return. Range: 1-100.
</ParamField>

<ParamField header="Authorization" type="string" required>
Bearer token for API authentication. Format: `Bearer YOUR_API_KEY`
</ParamField>

#### Response fields

Example of response field documentation:

<ResponseField name="user_id" type="string" required>
Unique identifier assigned to the newly created user.
</ResponseField>

<ResponseField name="created_at" type="timestamp">
ISO 8601 formatted timestamp of when the user was created.
</ResponseField>

<ResponseField name="permissions" type="array">
List of permission strings assigned to this user.
</ResponseField>

#### Expandable nested fields

Example of nested field documentation:

<ResponseField name="user" type="object">
Complete user object with all associated data.

<Expandable title="User properties">
  <ResponseField name="profile" type="object">
  User profile information including personal details.
  
  <Expandable title="Profile details">
    <ResponseField name="first_name" type="string">
    User's first name as entered during registration.
    </ResponseField>
    
    <ResponseField name="avatar_url" type="string | null">
    URL to user's profile picture. Returns null if no avatar is set.
    </ResponseField>
  </Expandable>
  </ResponseField>
</Expandable>
</ResponseField>

### Media and advanced components

#### Frames for images

Wrap all images in frames:

<Frame>
<img src="/images/dashboard.png" alt="Main dashboard showing analytics overview" />
</Frame>

<Frame caption="The analytics dashboard provides real-time insights">
<img src="/images/analytics.png" alt="Analytics dashboard with charts" />
</Frame>

#### Videos

Use the HTML video element for self-hosted video content:

<video
  controls
  className="w-full aspect-video rounded-xl"
  src="link-to-your-video.com"
></video>

Embed YouTube videos using iframe elements:

<iframe
  className="w-full aspect-video rounded-xl"
  src="https://www.youtube.com/embed/4KzFe50RQkQ"
  title="YouTube video player"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
></iframe>

#### Tooltips

Example of tooltip usage:

<Tooltip tip="Application Programming Interface - protocols for building software">
API
</Tooltip>

#### Updates

Use updates for changelogs:

<Update label="Version 2.1.0" description="Released March 15, 2024">
## New features
- Added bulk user import functionality
- Improved error messages with actionable suggestions

## Bug fixes
- Fixed pagination issue with large datasets
- Resolved authentication timeout problems
</Update>

## Required page structure

Every documentation page must begin with YAML frontmatter:

```yaml
---
title: "Clear, specific, keyword-rich title"
description: "Concise description explaining page purpose and value"
---
```

## Content quality standards

### Code examples requirements

- Always include complete, runnable examples that users can copy and execute
- Show proper error handling and edge case management
- Use realistic data instead of placeholder values
- Include expected outputs and results for verification
- Test all code examples thoroughly before publishing
- Specify language and include filename when relevant
- Add explanatory comments for complex logic
- Never include real API keys or secrets in code examples

### API documentation requirements

- Document all parameters including optional ones with clear descriptions
- Show both success and error response examples with realistic data
- Include rate limiting information with specific limits
- Provide authentication examples showing proper format
- Explain all HTTP status codes and error handling
- Cover complete request/response cycles

### Accessibility requirements

- Include descriptive alt text for all images and diagrams
- Use specific, actionable link text instead of "click here"
- Ensure proper heading hierarchy starting with H2
- Provide keyboard navigation considerations
- Use sufficient color contrast in examples and visuals
- Structure content for easy scanning with headers and lists

## Component selection logic

- Use **Steps** for procedures and sequential instructions
- Use **Tabs** for platform-specific content or alternative approaches
- Use **CodeGroup** when showing the same concept in multiple programming languages
- Use **Accordions** for progressive disclosure of information
- Use **RequestExample/ResponseExample** specifically for API endpoint documentation
- Use **ParamField** for API parameters, **ResponseField** for API responses
- Use **Expandable** for nested object properties or hierarchical information

---

# Framer to Mintlify MDX Conversion Rules

When converting Framer-exported HTML documents to Mintlify MDX format, follow these rules:

## Overview

Convert HTML documents from `AAA-Framer-Export/` folder into Mintlify MDX format, organized according to the provided information architecture. Download images from Framer URLs, rename them appropriately, and convert HTML content to markdown.

## File Structure Mapping

### Main Categories (from IA):

1. **Getting Started** - 3 subcategories (Providers, Staff, Billers) - *Note: No files mapped to this in current IA*
2. **Provider Workflows** - 6 subcategories
3. **Front Office Workflows** - 15 subcategories  
4. **Billing Workflows** - 4 subcategories
5. **Owners & Administration** - 2 subcategories

### Files Not in IA (to be flagged):

- `Navigating your lead tracker.txt`
- `Denials Worklist Page.txt`
- `The Claim Recon Page.txt`
- `Understanding Submission Errors.txt`
- `Understand Import Errors.txt`
- `How to Use Universal Search in Insights.txt`
- `How to Troubleshoot Login Issues.txt`
- `Navigating the Rejections Page.txt`
- `How (and When) to Use the Quick Purchase Function.txt` - *Note: This appears in Front Office > Appointments in the IA, but with different title format*

## Implementation Steps

### 1. File Mapping & Organization

- Parse all 178 `.txt` files in `AAA-Framer-Export/`
- Map each file to its location in the IA structure
- Create folder structure matching IA:
  - `Provider Workflows/Chart Notes/`
  - `Provider Workflows/AI Scribe & Tooling/`
  - `Front Office Workflows/Calendar/`
  - `Front Office Workflows/Appointments/`
  - etc.
- Generate a report of files not found in IA

### 2. Image Download & Processing

For each document:

- Extract all image URLs from HTML (pattern: `https://framerusercontent.com/images/[hash].png`)
- Download each image
- Create image folder structure mirroring full MDX folder structure: `images/[full-mdx-path]/[sanitized-article-title]/`
  - Example: If MDX is at `Provider Workflows/Chart Notes/getting-started-with-chart-notes.mdx`
  - Image folder: `images/Provider Workflows/Chart Notes/getting-started-with-chart-notes/`
- Rename images sequentially: `[sanitized-title]-1.png`, `[sanitized-title]-2.png`, etc.
- Store images in the appropriate subfolder

### 3. HTML to MDX Conversion

For each `.txt` file:

- Extract title (first line)
- Parse HTML content (from line 3 onwards)
- Convert HTML to markdown:
  - `<p>` → paragraph (blank line)
  - `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>` → `##`, `###`, `####`, `#####`, `######`
  - `<ul><li>` → markdown lists
  - `<ol><li>` → numbered lists
  - `<code>` → backticks
  - `<a href="...">` → `[text](url)`
  - `<strong>`, `<em>` → `**bold**`, `*italic*`
  - `<table>` → markdown tables (with proper header and data rows)
  - `<iframe>` (YouTube embeds) → properly formatted Mintlify iframe with required attributes
- **CRITICAL: Image Handling**
  - **DO NOT use markdown image syntax** `![alt](path)` - this causes images to display as plain text in Mintlify
  - **USE HTML img tags** with URL-encoded paths: `<img src="/images/...path..." alt="" />`
  - **URL-encode spaces and special characters** in image paths (spaces → `%20`, `&` → `%26`)
  - Example: `<img src="/images/Owners%20%26%20Administration/My%20Practice/article-title/article-title-1.png" alt="" />`
  - This ensures images display correctly instead of showing as plain text
- **CRITICAL: Table Conversion**
  - HTML tables must be converted to markdown table format
  - Tables wrapped in `<figure>` tags should also be converted
  - Example: `<table><tr><th>Header</th></tr><tr><td>Data</td></tr></table>` → markdown table
- **CRITICAL: Iframe/Video Conversion**
  - YouTube iframes must be converted to Mintlify format with proper attributes
  - Required attributes: `className`, `title`, `frameBorder`, `allow`, `allowFullScreen`
  - Example format:
    ```html
    <iframe
      className="w-full aspect-video rounded-xl"
      src="https://www.youtube.com/embed/VIDEO_ID"
      title="YouTube video player"
      frameBorder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowFullScreen
    ></iframe>
    ```
- For unconvertible HTML, keep as-is with comment: `<!-- HTML preserved: [reason] -->`
- Replace Framer image URLs with local paths: `/images/[full-mdx-path]/[article-title]/[article-title]-1.png`
  - Example: `/images/Provider Workflows/Chart Notes/getting-started-with-chart-notes/getting-started-with-chart-notes-1.png`

### 4. MDX File Generation

- Create `.mdx` files in appropriate folders
- Add frontmatter with title only:
  ```yaml
  ---
  title: "Article Title"
  ---
  ```
- Write converted markdown content
- Ensure proper file naming: `[article-title].mdx` (sanitized, lowercase, hyphens)

### 5. Image Path Resolution

- Calculate relative paths from MDX file location to image folder
- Update image references in MDX to use correct relative paths
- Image folder structure mirrors full MDX folder structure (including top-level categories)
- **CRITICAL: Use HTML img tags with URL-encoded paths**
- Example: If MDX is at `Provider Workflows/Chart Notes/getting-started-with-chart-notes.mdx`
  - Image at `images/Provider Workflows/Chart Notes/getting-started-with-chart-notes/getting-started-with-chart-notes-1.png`
  - Reference: `<img src="/images/Provider%20Workflows/Chart%20Notes/getting-started-with-chart-notes/getting-started-with-chart-notes-1.png" alt="" />`
  - Note: Spaces are URL-encoded as `%20` in the src attribute

## Technical Details

### Note on File Organization and Cursor's File Finding

Both folder structures (nested vs flat) work equally well for Cursor's file finding capabilities:

- **Cursor's semantic search** works the same regardless of folder structure - it searches by content, not location
- **File path search** (Ctrl/Cmd+P) works with both structures - you can type partial paths or filenames
- **Main benefits of nested structure:**
  - Better organization for humans browsing the file system
  - Avoids potential filename conflicts (e.g., if two different sections have articles with similar names)
  - Easier to understand context when viewing file paths
  - Mirrors the documentation structure, making it intuitive
- **Flat structure** would also work fine, but nested is generally preferred for maintainability

### File Name Sanitization

- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters (keep alphanumeric, hyphens, underscores)
- Handle edge cases (e.g., `Add_edit` → `add-edit`)

### Image Download Strategy

- Use Python `requests` library with `verify=False` to handle SSL issues with Framer URLs
- Disable SSL warnings using `urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)`
- Handle network errors gracefully - if download fails, keep original URL temporarily
- Preserve original image format (likely PNG)
- Validate downloaded images
- **After downloading, update MDX files to use HTML img tags with URL-encoded local paths**

### HTML Parsing

- Use HTML parser (BeautifulSoup for Python, cheerio for Node.js, or regex for simple cases)
- Handle nested structures (lists within lists)
- Preserve code blocks and inline code
- Handle empty alt text for images
- **Convert images to HTML img tags (not markdown syntax) with URL-encoded paths**
- **Convert HTML tables to markdown tables** - extract `<tr>`, `<th>`, `<td>` elements and format as markdown
- **Convert all heading levels** - `<h2>` through `<h6>` must be converted to markdown headings (`##` through `######`)
- **Convert iframes properly** - YouTube embeds must use Mintlify iframe format with all required attributes
- **Never preserve tables, headings, or iframes as HTML comments** - they must be converted to proper markdown/HTML format

## Output Structure

```
docs.athelas.com/
├── Getting Started
│   ├── Providers (healthcare clinicians)
│   ├── Staff (front desk, MAs)
│   └── Billers (RCM specialists)
│
├── Provider Workflows
│   ├── Chart Notes
│   │   ├── Getting Started with Chart Notes
│   │   ├── Auto-apply KX Modifier
│   │   ├── AI Appt. Summaries
│   │   ├── Chart Note Clinical Types
│   │   ├── Download Chart Notes as PDFs
│   │   ├── Goals on the chart note
│   │   ├── How to add Measurements
│   │   ├── Import Previous Medical History
│   │   ├── Navigating Flowsheets
│   │   ├── Navigating Inbox Workflows
│   │   ├── Navigating the Chart Note
│   │   ├── Set up Custom Chart Note Templates
│   │   ├── Setting up Co-signers on Your Note
│   │   ├── Sign a Chart Note
│   │   ├── Text Snippets For Your Note
│   │   └── Chart Note Features Not Supported
│   │
│   ├── AI Scribe & Tooling
│   │   ├── Additional Context Feature
│   │   ├── Complete a Visit with Air Scribe
│   │   ├── Edit with Command+K
│   │   ├── How to Apply an Air Scribe
│   │   ├── How to Set up AI Compliance
│   │   └── Setting up AI Compliance
│   │
│   ├── Calendar
│   │   ├── Getting started with the Calendar
│   │   └── Filter the calendar view
│   │
│   ├── Claim Details
│   │   └── Submissions and Remits
│   │
│   ├── Patient Profiles
│   │   ├── Getting started with Patient Profile
│   │   ├── Navigating Labs
│   │   ├── Add attachments to Patient Profile
│   │   ├── Prescribe Medications
│   │   ├── Record Allergies
│   │   ├── Record Immunizations
│   │   ├── View Patient's Appointments
│   │   └── Profile Features Not Supported
│   │
│   ├── Medications
│   │   └── Designate Staff as Provider Agents
│   │
│   └── Athelas Assistant
│       ├── Getting Started with Athelas Assistant
│       ├── Athelas Assistant Common Functionalities
│       └── Athelas Assistant Best Practices
│
├── Front Office Workflows
│   ├── Calendar
│   │   ├── Getting started with the Calendar
│   │   ├── Calendar start & end times
│   │   ├── Filter the calendar view
│   │   ├── Modify calendar views
│   │   ├── Viewing multiple providers
│   │   └── Features not supported
│   │
│   ├── Appointments
│   │   ├── The Insights Appointments Page
│   │   ├── Adding Prior Auth and Alerting
│   │   ├── Alternate Methods for Scheduling
│   │   ├── How to Add a Walk-In Patient
│   │   ├── How to Run an Eligibility Check
│   │   ├── How to Schedule an Appointment
│   │   ├── How to Take Payments
│   │   ├── Sending out reminders and forms
│   │   ├── Understanding Appointment Details
│   │   ├── Updating Appointment Statuses
│   │   └── Appt. Features not supported
│   │
│   ├── Agents Center
│   │   ├── Getting Started with Agents Center
│   │   ├── Components of the Dashboard
│   │   ├── Make an Outbound Call
│   │   └── Understanding Use Cases
│   │
│   ├── Claim Details
│   │   ├── Claim Details Page
│   │   ├── Other Submission Types (Secondary, Specialty etc)
│   │   ├── Encounter Timeline for Claims
│   │   ├── How to Download CMS-1500 Forms
│   │   ├── How to Resubmit a Single Claim
│   │   ├── How to Resubmit Claims in Bulk
│   │   ├── How to Send Documentation
│   │   └── Submissions and Remits
│   │
│   ├── Daily Operations
│   │   └── How to Reconcile Your Cash Drawer
│   │
│   ├── Encounter Details
│   │   ├── Encounter Details Page
│   │   ├── Insights Prior Authorization
│   │   ├── Encounter Stage and Status
│   │   └── How to Update Insurance
│   │
│   ├── Faxing
│   │   ├── Getting Started with Faxing
│   │   ├── Attach Task Follow-ups to Faxes
│   │   ├── Send and Receive a Fax
│   │   ├── Tying Faxes to Patients
│   │   ├── Tying inbound faxes to outbound faxes
│   │   └── Faxing Features Not Supported
│   │
│   ├── Messaging
│   │   ├── How to receive messages
│   │   ├── How to send messages
│   │   └── Messages Page
│   │
│   ├── Patient Communications
│   │   ├── General Patient Flows Features
│   │   ├── Text Blast Page
│   │   ├── Insurance Intake Page
│   │   ├── Functional Outcome Measurements
│   │   ├── Getting Started with Patient Portal
│   │   ├── Complete Intake Forms
│   │   ├── Navigating Patient Workflows
│   │   ├── Manage Patient Appointments
│   │   ├── Manage Payments through Patient Portal
│   │   ├── Patient Intake Automation
│   │   ├── Update Insurance Info
│   │   └── View Home Exercise Programs
│   │
│   ├── Patient Demographics
│   │   ├── Getting Started with Demographics
│   │   ├── Add/edit a Patient's Insurance
│   │   ├── Add/edit Patient Cases
│   │   └── Add/edit Patient's Prior Authorization
│   │
│   ├── Patient Profiles
│   │   ├── How to Find and Edit a Patient's Profile
│   │   └── How to Resubmit Claim(s)
│   │
│   ├── Patient Responsibility
│   │   ├── Patient Responsibility Page
│   │   ├── Charge Saved Credit Cards
│   │   ├── Manage Credit Cards
│   │   ├── Setting up a Payment Plan
│   │   ├── How to Cancel PR
│   │   ├── How to Send a Patient Payment Link
│   │   ├── How to Push to PR
│   │   ├── How to Record Payments
│   │   ├── How to Refund a Payment
│   │   ├── How to Request via Text or Email
│   │   ├── How to Set Up Miscellaneous Line Item Charges
│   │   ├── How to Take Payment for Families
│   │   ├── How to Undo a Write Off
│   │   ├── How to Write Off PR
│   │   ├── PR Overpayment Refunds and Estimated vs. Remittance PR
│   │   ├── PR Settings
│   │   └── PR Timeline
│   │
│   ├── Patient Statements
│   │   ├── Turn off Patient Texts
│   │   ├── How to Spread PR Statement Emails
│   │   ├── Manage Patient Statements
│   │   ├── Print Patient Statements
│   │   ├── Send Email Statements
│   │   ├── Send One-off Paper Statements
│   │   └── Send Patient Statements via Email/Text
│   │
│   ├── Posting
│   │   ├── How to Handle Duplicate Remittances
│   │   ├── How to Handle Partial Denials
│   │   ├── How to Post a Remittance Manually
│   │   ├── How to Use the Posting Tool Page
│   │   └── How to Write Off a Balance
│   │
│   ├── Tasking
│   │   ├── How to create tasks
│   │   └── Sorting, Archiving, Bulk Actions
│   │
│   ├── Utilities
│   │   ├── Self-service Credentialing
│   │   ├── Patient Subscriptions
│   │   ├── Process Virtual Cards
│   │   ├── Download EDI's in Bulk
│   │   ├── Bank Deposit Verification
│   │   └── EOB Creation and Portal Checks
│   │
│   └── Athelas Assistant
│       ├── Getting Started With Your RCM Assistant
│       └── RCM AI Prompt Library
│
├── Billing Workflows
│   ├── Analytics
│   │   ├── The Denials Analysis Page
│   │   └── The Revenue Analysis Page
│   │
│   ├── Front Office Payments
│   │   ├── How to Create Suggested PR Rules
│   │   ├── Self-pay Fee Schedule
│   │   └── Target Allowed Amounts
│   │
│   ├── General Billing
│   │   ├── Remittances
│   │   ├── How to Set Block PR Rules
│   │   ├── The Billing Rules Engine
│   │   └── The Review Charges Page
│   │
│   ├── Reports
│   │   ├── Building and Running Reports
│   │   ├── A/R Reports
│   │   ├── Claim Adjustments Report
│   │   ├── Collections Report
│   │   ├── Custom Collections Report
│   │   ├── Detailed Charges Report
│   │   ├── Export Claim Details
│   │   ├── Generate a Transaction Report
│   │   ├── Patient Balances Report
│   │   ├── Patient Charges Report
│   │   ├── Patient Claims One-pagers
│   │   ├── Patient Collections Report
│   │   ├── Patient Eligibility Report
│   │   ├── Posting Log Report
│   │   ├── Site Transaction Report
│   │   ├── Site Transaction Report Summary
│   │   ├── Submitted Claims Report
│   │   └── Upcoming Patient Statements Report
│   │
│   └── Athelas Assistant
│       ├── Getting Started With Your RCM Assistant
│       └── RCM AI Prompt Library
│
└── Owners & Administration
    ├── My Practice
    │   ├── Getting Started with Your Practice
    │   ├── Your Athelas Invoice
    │   ├── Manage Staff & Permissions
    │   └── Update Practice Information
    │
    └── Reporting
        └── Measuring Performance
```

## Files to Flag (Not in IA)

Create a `UNMAPPED_FILES.md` report listing:

- `Navigating your lead tracker.txt`
- `Denials Worklist Page.txt`
- `The Claim Recon Page.txt`
- `Understanding Submission Errors.txt`
- `Understand Import Errors.txt`
- `How to Use Universal Search in Insights.txt`
- `How to Troubleshoot Login Issues.txt`
- `Navigating the Rejections Page.txt`

## Critical Implementation Notes

### Image Display Fix (Learned from Owners & Administration migration)

**Problem:** Images were displaying as plain text instead of rendering in Mintlify.

**Root Cause:** 
- Markdown image syntax `![alt](path)` doesn't work well with URL-encoded paths containing spaces
- Mintlify requires HTML img tags when paths contain spaces or special characters

**Solution:**
1. Use HTML `<img>` tags instead of markdown `![]()` syntax
2. URL-encode spaces (`%20`) and special characters (`&` → `%26`) in the `src` attribute
3. Example: `<img src="/images/Owners%20%26%20Administration/My%20Practice/article/article-1.png" alt="" />`

**Why this works:**
- HTML attributes handle URL encoding better than markdown
- Mintlify's image rendering works correctly with URL-encoded paths in HTML tags
- This prevents images from displaying as plain text

### Parsing Error Fixes (Learned from Provider Workflows migration)

**Problem:** Several pages showed parsing errors with HTML tags preserved as comments instead of being converted.

**Root Causes:**
1. **Tables:** HTML `<table>` tags were preserved as comments instead of being converted to markdown tables
2. **Headings:** `<h2>` and `<h5>` tags were preserved as comments instead of being converted to markdown headings
3. **Iframes:** YouTube iframe embeds were preserved as comments instead of being formatted for Mintlify

**Solutions:**
1. **Tables:** Convert HTML tables to markdown table format
   - Extract `<tr>`, `<th>`, `<td>` elements
   - Build markdown table with proper header row and separator
   - Handle tables wrapped in `<figure>` tags
2. **Headings:** Convert all heading levels (`<h2>` through `<h6>`) to markdown headings (`##` through `######`)
3. **Iframes:** Convert YouTube iframes to Mintlify format with required attributes:
   - `className="w-full aspect-video rounded-xl"`
   - `title="YouTube video player"`
   - `frameBorder="0"`
   - `allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"`
   - `allowFullScreen`

**Why this matters:**
- HTML comments don't render in Mintlify, causing parsing errors
- Tables, headings, and videos must be in proper format to display correctly
- The conversion script now handles all these cases automatically

### Universal Script

Use `convert_framer_to_mdx.py` for all categories. The script:
- Handles image downloads with SSL verification disabled (required for Framer URLs)
- Converts HTML to MDX with proper image tag formatting
- Converts HTML tables to markdown tables
- Converts all heading levels (h2-h6) to markdown headings
- Converts YouTube iframes to proper Mintlify format
- Creates correct folder structure matching IA
- URL-encodes image paths automatically

## Error Handling

- Log any files that fail to parse
- Log any images that fail to download
- Preserve original files in `AAA-Framer-Export/` (don't delete)
- Create error report for manual review
- If images don't display, check that HTML img tags are used with URL-encoded paths

## Validation

- Verify all 178 files are processed
- Verify all images are downloaded
- Verify MDX files are valid (can be checked with Mintlify CLI)
- Verify image paths are correct relative to MDX files
- **Verify images display correctly** (not as plain text) - if they show as text, check that HTML img tags with URL-encoded paths are used

## Universal Conversion Script

Use `convert_framer_to_mdx.py` for all category conversions. The script:

1. **Handles all categories** - Provider, Front Office, Billing, Owners & Administration
2. **Automatic image handling:**
   - Downloads images from Framer URLs
   - Creates proper folder structure
   - Uses HTML img tags with URL-encoded paths (fixes display issues)
3. **HTML to MDX conversion:**
   - Converts all HTML elements to markdown
   - Handles nested lists properly
   - Preserves formatting (bold, italic, code, links)
4. **Proper file organization:**
   - Creates folder structure matching IA
   - Sanitizes filenames correctly
   - Adds proper frontmatter

### Usage

```bash
python3 convert_framer_to_mdx.py <category>
```

Categories: `owners-admin`, `provider`, `front-office`, `billing`, `all`

### Setting Up File Mappings

Before running, populate the `load_file_mapping()` function with the file mappings based on the IA structure. Each entry should map:
- `.txt` filename → category, subcategory, and title

Example:
```python
{
    "Getting Started with Chart Notes.txt": {
        "category": "Provider Workflows",
        "subcategory": "Chart Notes",
        "title": "Getting Started with Chart Notes"
    },
    ...
}
```

### Key Features

- **SSL handling:** Disables SSL verification for Framer image downloads
- **URL encoding:** Automatically URL-encodes image paths for Mintlify compatibility
- **Error handling:** Gracefully handles download failures
- **Progress reporting:** Shows download and conversion progress

