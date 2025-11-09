# Multi-Platform Integration API Quick Reference

## 🚀 Quick Start Checklist

- [ ] Install dependencies: `pip install groq python-dotenv requests`
- [ ] Set up Google Sheets API (follow guide below)
- [ ] Get Serper API key → https://serper.dev
- [ ] Get Groq API key → https://console.groq.com
- [ ] Add keys to `.env` file
- [ ] Run test: `python test_multi_platform_integration.py`

---

## 📝 Environment Variables (.env file)

```env
# Required for Serper
SERPER_API_KEY=your_serper_key_here

# Required for Groq
GROQ_API_KEY=your_groq_key_here

# Google Sheets (credentials file path)
GOOGLE_SHEETS_CREDENTIALS=config/google_credentials.json
```

---

## 1️⃣ Google Sheets API

### Setup Steps (5 minutes)

1. **Go to Google Cloud Console**
   - https://console.cloud.google.com/

2. **Create/Select Project**
   - Click "Select a project" → "New Project"
   - Name: `compliance-checker`

3. **Enable APIs**
   - Go to "APIs & Services" → "Library"
   - Enable: "Google Sheets API"
   - Enable: "Google Drive API"

4. **Create Service Account**
   - "APIs & Services" → "Credentials"
   - "Create Credentials" → "Service Account"
   - Name: `compliance-checker`
   - Click through and create

5. **Generate Key**
   - Click on service account
   - "Keys" tab → "Add Key" → "Create new key"
   - Choose JSON → Download

6. **Install Credentials**
   ```powershell
   # Copy to config folder
   Copy-Item "Downloads\your-key.json" "config\google_credentials.json"
   ```

7. **Share Sheets**
   - Open your Google Sheet
   - Click "Share"
   - Add service account email (from JSON file)
   - Give "Editor" permission

### Usage

```python
from services.google_sheets_service import GoogleSheetsService
from services.google_sheets_writer import GoogleSheetsWriter

# Read from sheet
sheets = GoogleSheetsService()
text = sheets.extract_text_from_sheet(
    url="https://docs.google.com/spreadsheets/d/SHEET_ID/edit",
    sheet_name="Contract",
    cell_range="A1:B100"
)

# Write to sheet
writer = GoogleSheetsWriter()
sheet_id = writer.create_new_spreadsheet("Compliance Report")
writer.write_compliance_report(sheet_id, report_data)
```

### Service Account Email Location
Open `config/google_credentials.json` and find:
```json
{
  "client_email": "compliance-checker@project-id.iam.gserviceaccount.com"
}
```

---

## 2️⃣ Serper API (Google Search)

### Setup (2 minutes)

1. **Sign Up**
   - Go to https://serper.dev
   - Sign up with Google or Email

2. **Get API Key**
   - Dashboard shows your API key
   - Copy it

3. **Add to .env**
   ```env
   SERPER_API_KEY=your_key_here
   ```

### Free Tier
- 2,500 searches/month FREE
- No credit card required

### Usage

```python
from services.serper_service import SerperService

serper = SerperService()

# Search regulatory updates
updates = serper.search_regulatory_updates("GDPR", year=2025)

# Search case studies
cases = serper.search_compliance_case_studies("HIPAA", industry="healthcare")

# Verify requirements
verification = serper.verify_requirement(
    "Data processing must have legal basis",
    "GDPR"
)

# Get news
news = serper.get_regulatory_news(["GDPR", "HIPAA"], days=30)
```

---

## 3️⃣ Groq API (Fast LLM)

### Setup (2 minutes)

1. **Sign Up**
   - Go to https://console.groq.com
   - Sign up with Google or Email

2. **Create API Key**
   - Dashboard → "API Keys"
   - Click "Create API Key"
   - Name it: `compliance-checker`
   - **Copy immediately** (won't show again!)

3. **Add to .env**
   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```

### Free Tier
- 14,400 requests/day FREE
- Very fast inference
- Multiple models available

### Available Models
- `mixtral-8x7b-32768` - Fast, balanced (recommended)
- `llama3-70b-8192` - Most powerful
- `llama3-8b-8192` - Fastest

### Usage

```python
from services.groq_service import GroqService

groq = GroqService()

# Generate compliant clause
clause = groq.generate_compliant_clause(
    clause_type="Data Processing",
    framework="GDPR",
    context="Cloud storage provider",
    issues=["Missing data retention policy"]
)

# Analyze risk
analysis = groq.analyze_compliance_risk(
    clause_text="We process your data as needed",
    framework="GDPR"
)

# Generate summary
summary = groq.generate_compliance_summary(
    report_data=results,
    frameworks=["GDPR", "HIPAA"]
)

# Compare frameworks
comparison = groq.compare_frameworks(
    clause_text="Your clause here",
    frameworks=["GDPR", "HIPAA", "CCPA"]
)
```

---

## 4️⃣ Notification System

### Usage

```python
from services.notification_system import (
    NotificationSystem,
    NotificationType,
    NotificationSeverity
)

notif = NotificationSystem()

# Send high-risk alert
notif.notify_high_risk_clause(
    clause_id="C001",
    clause_text="Problematic clause",
    risk_level="high",
    frameworks=["GDPR"],
    issues=["Missing consent mechanism"]
)

# Notify missing requirements
notif.notify_missing_requirements(
    framework="HIPAA",
    missing_count=3,
    requirements=requirements_list
)

# Notify analysis complete
notif.notify_analysis_complete(
    overall_score=78.5,
    total_clauses=15,
    high_risk_count=2,
    frameworks=["GDPR", "HIPAA"]
)

# Get report
report = notif.generate_notification_report()
```

---

## 🔧 Testing

### Test All Connections
```powershell
python test_multi_platform_integration.py
```

### Test Individual Services
```python
# Test Google Sheets
from services.google_sheets_service import GoogleSheetsService
sheets = GoogleSheetsService()
sheets.test_connection()  # Returns True if working

# Test Serper
from services.serper_service import SerperService
serper = SerperService()
serper.test_connection()  # Returns True if working

# Test Groq
from services.groq_service import GroqService
groq = GroqService()
groq.test_connection()  # Returns True if working
```

---

## 📊 Complete Workflow Example

```python
from services.google_sheets_service import GoogleSheetsService
from services.google_sheets_writer import GoogleSheetsWriter
from services.serper_service import SerperService
from services.groq_service import GroqService
from services.notification_system import NotificationSystem
from services.compliance_checker import ComplianceChecker

# 1. Read contract from Google Sheets
sheets = GoogleSheetsService()
contract_text = sheets.extract_text_from_sheet(
    url="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
)

# 2. Analyze compliance
checker = ComplianceChecker()
results = checker.check_compliance(clauses, ["GDPR", "HIPAA"])

# 3. Generate enhanced recommendations with Groq
groq = GroqService()
for clause in results['non_compliant']:
    enhanced = groq.generate_compliant_clause(
        clause_type=clause['type'],
        framework=clause['framework'],
        current_clause=clause['text'],
        issues=clause['issues']
    )
    clause['enhanced_recommendation'] = enhanced

# 4. Search for regulatory updates
serper = SerperService()
updates = serper.search_regulatory_updates("GDPR", year=2025)

# 5. Write report to Google Sheets
writer = GoogleSheetsWriter()
report_sheet_id = writer.create_new_spreadsheet("Compliance Report")
writer.write_compliance_report(report_sheet_id, results)

# 6. Send notifications
notif = NotificationSystem()
notif.notify_analysis_complete(
    overall_score=results['overall_score'],
    total_clauses=len(clauses),
    high_risk_count=results['high_risk_count'],
    frameworks=["GDPR", "HIPAA"],
    spreadsheet_id=report_sheet_id
)

print(f"✓ Complete! Report: https://docs.google.com/spreadsheets/d/{report_sheet_id}")
```

---

## 🛠️ Troubleshooting

### Google Sheets: "Permission Denied"
- **Solution**: Share sheet with service account email from `google_credentials.json`

### Serper: "Invalid API Key"
- **Solution**: Check `.env` file, ensure no spaces in key

### Groq: "Authentication Failed"
- **Solution**: Verify key starts with `gsk_`, regenerate if needed

### Import Errors
```powershell
pip install --upgrade groq google-auth google-api-python-client requests
```

---

## 💰 Cost Summary

| Service | Free Tier | Notes |
|---------|-----------|-------|
| Google Sheets API | Unlimited | Completely free |
| Serper API | 2,500 searches/mo | Credit card not required |
| Groq API | 14,400 req/day | Very generous limit |

**Total Monthly Cost with Free Tiers: $0** 🎉

---

## 📚 Documentation Files

- **Setup Guide**: `MULTI_PLATFORM_INTEGRATION_GUIDE.md`
- **Google Sheets**: `config/GOOGLE_SHEETS_SETUP.md`
- **Usage Examples**: `example_multi_platform_usage.py`
- **Test Script**: `test_multi_platform_integration.py`

---

## 🚀 Next Steps

1. Complete API setups (15 minutes total)
2. Run `python test_multi_platform_integration.py`
3. Try examples: `python example_multi_platform_usage.py`
4. Integrate into your Streamlit app
5. Start analyzing contracts!

---

**Questions?** Check the full guide: `MULTI_PLATFORM_INTEGRATION_GUIDE.md`
