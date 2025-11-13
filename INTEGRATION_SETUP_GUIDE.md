# Multi-Platform Integration Setup Guide

## 🚀 Overview

Your AI-Powered Regulatory Compliance Checker now includes comprehensive multi-platform integrations for automated compliance workflow.

## 📋 New Features Added

### 1. **Slack Integration** 
- Real-time alerts for high-risk contracts (Risk Score > 80)
- Contract expiration warnings (< 30 days)
- Regulatory update notifications
- Compliance report summaries

### 2. **Email Notifications**
- High-risk contract alerts with detailed analysis
- Amendment suggestion emails to legal team
- Daily/weekly compliance reports
- Supports SendGrid, Mailgun, and SMTP

### 3. **Google Sheets Sync**
- **Bi-directional** data flow
- Read contract metadata from master spreadsheet
- Auto-update compliance status to dedicated tab
- Formatted reports with charts

### 4. **Regulatory Update Tracking**
- Monitors SEC Edgar filings
- EUR-Lex for GDPR updates
- Daily automated polling
- NLP keyword extraction
- Urgency scoring (0-100)

### 5. **Contract Modification Module**
- Maps regulatory changes to contract clauses
- AI-powered amendment suggestions (OpenAI integration)
- Template-based fallback
- Side-by-side diff comparison
- Auto-apply for simple changes

### 6. **Integration Orchestrator**
- Coordinates all services
- Daily compliance workflow automation
- Batch processing
- Centralized logging

## ⚙️ Configuration

### Step 1: Install Additional Dependencies

```powershell
cd "d:\5thSEM\new update\jaggu-proj"
pip install spacy sendgrid openai
python -m spacy download en_core_web_sm
```

### Step 2: Configure Environment Variables

Create or update `.env` file in project root:

```env
# Slack Integration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#compliance-alerts
SLACK_RISK_THRESHOLD=80
SLACK_EXPIRY_WARNING_DAYS=30

# Email Configuration (Choose one)
EMAIL_SERVICE=smtp  # Options: smtp, sendgrid, mailgun

# SMTP Configuration (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
EMAIL_FROM=compliance@yourcompany.com
LEGAL_TEAM_EMAIL=legal@yourcompany.com

# SendGrid (Alternative)
SENDGRID_API_KEY=your_sendgrid_api_key

# Mailgun (Alternative)
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=mg.yourcompany.com

# Google Sheets Integration
GOOGLE_SHEETS_CREDENTIALS_PATH=./config/google-sheets-credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_COMPLIANCE_TAB=Compliance_Status

# Regulatory APIs
SEC_EDGAR_API_URL=https://www.sec.gov/cgi-bin/browse-edgar
REGULATORY_USER_AGENT=YourCompany-ComplianceBot/1.0 (your-email@company.com)
POLLING_INTERVAL_HOURS=24

# OpenAI (Optional - for AI-powered amendments)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.3
```

### Step 3: Set Up Slack Webhook

1. Go to your Slack workspace
2. Navigate to **Settings & Administration** > **Manage Apps**
3. Search for "Incoming Webhooks"
4. Click "Add to Slack"
5. Select channel: `#compliance-alerts` (or create one)
6. Copy the Webhook URL
7. Paste into `.env` file

### Step 4: Set Up Google Sheets

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Google Sheets API**
4. Create **Service Account** credentials
5. Download JSON credentials file
6. Save as `config/google-sheets-credentials.json`
7. Share your spreadsheet with the service account email
8. Copy spreadsheet ID from URL and add to `.env`

### Step 5: Set Up Email Service

#### Option A: Gmail (SMTP)
1. Enable 2-factor authentication on Gmail
2. Generate App-Specific Password
3. Use in `SMTP_PASSWORD` variable

#### Option B: SendGrid
1. Sign up at [SendGrid.com](https://sendgrid.com/)
2. Create API key
3. Add to `.env` file

#### Option C: Mailgun
1. Sign up at [Mailgun.com](https://www.mailgun.com/)
2. Verify domain
3. Get API key and add to `.env`

### Step 6: Configure OpenAI (Optional)

1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Generate API key
3. Add to `.env` file
4. Enable in orchestrator: `use_ai=True`

## 🎯 Usage Examples

### Example 1: Test Slack Notification

```python
from services.slack_notification_service import SlackNotificationService

slack = SlackNotificationService()

if slack.is_enabled():
    slack.notify_high_risk_contract(
        contract_name="Test Contract",
        risk_score=95,
        compliance_issues=[
            {"severity": "high", "description": "Missing GDPR clauses"}
        ]
    )
```

### Example 2: Send Email Alert

```python
from services.email_notification_service import EmailNotificationService

email = EmailNotificationService()

email.send_high_risk_alert(
    contract_name="Data Processing Agreement",
    risk_score=87,
    compliance_issues=[
        {"clause": "Article 28", "description": "Missing processor obligations"}
    ],
    recommendations=["Add GDPR Article 28 compliance clauses"]
)
```

### Example 3: Sync with Google Sheets

```python
from services.google_sheets_compliance_sync import GoogleSheetsComplianceSync

sheets = GoogleSheetsComplianceSync()

if sheets.is_enabled():
    sheets.write_compliance_status(
        contract_name="Service Agreement - ABC Ltd",
        compliance_data={
            'risk_score': 72,
            'compliance_status': 'Needs Review',
            'frameworks_checked': 'GDPR, CCPA',
            'issues_found': 3,
            'high_risk_issues': 1,
            'recommendations': 'Review data transfer clauses'
        }
    )
```

### Example 4: Track Regulatory Updates

```python
from services.regulatory_update_tracker import RegulatoryUpdateTracker

tracker = RegulatoryUpdateTracker()

# Fetch updates from all sources
updates = tracker.fetch_all_updates()

for update in updates:
    print(f"New regulation: {update['title']}")
    keywords = tracker.extract_keywords_from_update(update)
    urgency = tracker.calculate_urgency_score(update)
    print(f"Keywords: {keywords}")
    print(f"Urgency: {urgency}/100")
```

### Example 5: Generate Contract Amendments

```python
from services.contract_modification_engine import ContractModificationEngine

engine = ContractModificationEngine()

clause = {
    'id': 'clause-123',
    'clause_number': '5.2',
    'clause_title': 'Data Processing',
    'clause_text': 'Current clause text...',
    'clause_type': 'data_processing'
}

regulation = {
    'regulation_id': 'GDPR-2024-001',
    'title': 'Updated Data Processing Requirements',
    'description': 'New breach notification timelines',
    'keywords': ['data', 'processing', 'breach', 'notification'],
    'applicable_domain': 'GDPR',
    'jurisdiction': 'EU',
    'severity': 'high'
}

# Generate amendment
amendment = engine.generate_amendment_suggestion(
    clause=clause,
    regulation=regulation,
    use_ai=True  # Uses OpenAI if configured
)

print(f"Amendment ID: {amendment['amendment_id']}")
print(f"Suggested text: {amendment['suggested_text']}")
print(f"Confidence: {amendment['confidence_score']}")
```

### Example 6: Run Daily Compliance Check

```python
from services.compliance_integration_orchestrator import ComplianceIntegrationOrchestrator

orchestrator = ComplianceIntegrationOrchestrator()

# Your contracts (from database or file)
contracts = [
    {
        'name': 'Contract A',
        'risk_score': 85,
        'compliance_issues': [...],
        'frameworks': ['GDPR', 'CCPA'],
        'expiry_date': '2025-12-31'
    }
]

# Run complete workflow
results = orchestrator.run_daily_compliance_check(contracts)

print(f"Processed {results['total_contracts']} contracts")
print(f"Found {len(results['high_risk_contracts'])} high-risk contracts")
print(f"Generated {len(results['amendments_generated'])} amendments")
```

## 🔄 Automated Workflow

The orchestrator provides end-to-end automation:

1. **Morning** (Daily)
   - Fetch regulatory updates from APIs
   - Extract keywords using NLP
   - Calculate urgency scores

2. **Process Contracts**
   - Check each contract against new regulations
   - Map regulations to affected clauses
   - Calculate risk scores

3. **Generate Amendments**
   - Create AI-powered suggestions
   - Save to database
   - Calculate confidence scores

4. **Send Notifications**
   - Slack alerts for high-risk items
   - Email legal team with amendments
   - Update Google Sheets status

5. **Generate Reports**
   - Daily summary email
   - Google Sheets dashboard
   - Compliance metrics

## 📊 Google Sheets Structure

### Master Sheet: "Contracts"
| Contract Name | Party A | Party B | Effective Date | Expiry Date | Jurisdiction | Domains |
|---------------|---------|---------|----------------|-------------|--------------|---------|
| Agreement 1   | Acme    | Beta    | 2024-01-01    | 2025-12-31  | US          | GDPR    |

### Auto-Generated: "Compliance_Status"
| Contract Name | Risk Score | Status | Frameworks | Issues | High Risk | Last Checked | Recommendations |
|---------------|------------|--------|------------|--------|-----------|--------------|-----------------|
| Agreement 1   | 85.0       | Non-Compliant | GDPR, CCPA | 5 | 2 | 2025-11-09 10:30 | Review clauses |

## 🔐 Security Best Practices

1. **Never commit** `.env` file to Git
2. Use **service accounts** for Google Sheets (not personal accounts)
3. **Rotate API keys** regularly
4. **Restrict** Slack webhook to specific channels
5. Use **App Passwords** for Gmail, not main password
6. **Monitor** API usage and set quotas
7. **Enable** logging for audit trails

## 🧪 Testing

Test each integration before production:

```powershell
# Test Slack
python -c "from services.slack_notification_service import SlackNotificationService; s = SlackNotificationService(); print('Enabled:', s.is_enabled())"

# Test Email
python -c "from services.email_notification_service import EmailNotificationService; e = EmailNotificationService(); print('Configured')"

# Test Google Sheets
python -c "from services.google_sheets_compliance_sync import GoogleSheetsComplianceSync; g = GoogleSheetsComplianceSync(); print('Enabled:', g.is_enabled())"
```

## 📝 New Files Created

```
services/
├── slack_notification_service.py              # Slack webhooks
├── email_notification_service.py              # Email alerts
├── google_sheets_compliance_sync.py           # Bi-directional sync
├── regulatory_update_tracker.py               # API monitoring
├── contract_modification_engine.py            # Amendment generation
└── compliance_integration_orchestrator.py     # Workflow coordination
```

## 🚀 Next Steps

1. Configure environment variables
2. Set up each integration service
3. Test individual services
4. Run orchestrator for full workflow
5. Schedule daily checks (use Windows Task Scheduler or cron)
6. Monitor logs in `logs/` directory

## 📞 Support

For issues:
- Check logs in `logs/` directory
- Verify API credentials
- Test network connectivity
- Review environment variables

---

**Your compliance system is now fully integrated with multiple platforms! 🎉**
