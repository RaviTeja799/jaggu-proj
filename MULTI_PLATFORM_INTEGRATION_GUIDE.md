# Multi-Platform Integration Setup Guide

## Overview

This guide will help you integrate the AI Compliance Checker with:
1. **Google Sheets API** - Read contracts & Write compliance reports
2. **Serper API** - Web search for regulatory updates
3. **Groq API** - Fast LLM inference for enhanced recommendations

---

## 1. Google Sheets API Setup

### Step-by-Step Guide

#### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: `compliance-checker-integration`
4. Click "Create"

#### 1.2 Enable Google Sheets API

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for "**Google Sheets API**"
3. Click on it and press **Enable**
4. Also enable "**Google Drive API**" (for better access)

#### 1.3 Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **Service Account**
3. Fill in:
   - **Service account name**: `compliance-checker`
   - **Service account ID**: (auto-generated)
   - **Description**: `Service account for AI Compliance Checker`
4. Click **CREATE AND CONTINUE**
5. **Grant this service account access** (optional - skip)
6. Click **CONTINUE** → **DONE**

#### 1.4 Generate JSON Credentials

1. Click on the service account you just created
2. Go to **KEYS** tab
3. Click **ADD KEY** → **Create new key**
4. Select **JSON** format
5. Click **CREATE**
6. The file will download automatically (e.g., `compliance-checker-xxxxx.json`)

#### 1.5 Install Credentials in Project

```powershell
# Copy the downloaded file to config folder and rename it
Copy-Item "Downloads\compliance-checker-xxxxx.json" "E:\323103310024\Updated Infosys\jaggu-proj\config\google_credentials.json"
```

#### 1.6 Get Service Account Email

Open the `google_credentials.json` file and find the email:
```json
{
  "client_email": "compliance-checker@your-project.iam.gserviceaccount.com"
}
```

Copy this email - you'll need it to share sheets!

#### 1.7 Share Your Google Sheets

For EVERY Google Sheet you want to use:

1. Open the Google Sheet
2. Click **Share** button (top right)
3. Paste the service account email
4. Set permission to **Editor** (for writing reports) or **Viewer** (for reading only)
5. Uncheck "Notify people"
6. Click **Share**

---

## 2. Serper API Setup

### What is Serper API?
Serper API provides Google search results via API - useful for finding latest regulatory updates and compliance news.

### Step-by-Step Guide

#### 2.1 Create Serper Account

1. Go to [https://serper.dev/](https://serper.dev/)
2. Click **Sign Up** or **Get Started**
3. Sign up with Google or Email

#### 2.2 Get API Key

1. After login, go to **Dashboard**
2. You'll see your **API Key** displayed
3. Copy the API key (looks like: `a1b2c3d4e5f6...`)

#### 2.3 Add to Environment File

Open `.env` file and add:
```env
SERPER_API_KEY=your_serper_api_key_here
```

#### 2.4 Pricing

- **Free Tier**: 2,500 free searches
- **Paid Plans**: $50/month for 5,000 searches

---

## 3. Groq API Setup

### What is Groq API?
Groq provides ultra-fast LLM inference (70B models at high speed) - great for real-time compliance recommendations.

### Step-by-Step Guide

#### 3.1 Create Groq Account

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Click **Sign In** or **Get Started**
3. Sign up with Google or Email

#### 3.2 Get API Key

1. After login, go to **API Keys** section
2. Click **Create API Key**
3. Give it a name: `compliance-checker`
4. Copy the API key (looks like: `gsk_...`)
5. **Save it immediately** - you won't see it again!

#### 3.3 Add to Environment File

Open `.env` file and add:
```env
GROQ_API_KEY=your_groq_api_key_here
```

#### 3.4 Available Models

- `mixtral-8x7b-32768` - Fast, good for most tasks
- `llama3-70b-8192` - Most powerful
- `llama3-8b-8192` - Fastest

#### 3.5 Pricing

- **Free Tier**: 14,400 requests per day
- Very generous free tier!

---

## 4. Update .env File

Your complete `.env` file should look like:

```env
# Application Configuration
DEBUG=False
LOG_LEVEL=INFO

# Model Configuration
LEGAL_BERT_MODEL=nlpaueb/legal-bert-base-uncased
LLAMA_MODEL=meta-llama/Llama-2-13b-chat-hf
SENTENCE_TRANSFORMER_MODEL=sentence-transformers/all-MiniLM-L6-v2
USE_GPU=True

# Processing Configuration
MAX_FILE_SIZE_MB=10
OCR_LANGUAGE=eng
CONFIDENCE_THRESHOLD=0.75

# API Keys
OPENAI_API_KEY=
SERPER_API_KEY=your_serper_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS=config/google_credentials.json

# Notification Settings
ENABLE_NOTIFICATIONS=True
NOTIFICATION_EMAIL=your-email@example.com
```

---

## 5. Install Additional Dependencies

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install new packages
pip install groq python-dotenv requests
```

---

## 6. Test Connections

Run the test script to verify all APIs are working:

```powershell
python test_multi_platform_integration.py
```

---

## 7. Features Enabled

Once set up, you'll have:

### Google Sheets Integration
✅ Read contracts from Google Sheets  
✅ Write compliance reports to new sheets  
✅ Update existing sheets with results  
✅ Auto-generate summary sheets  

### Serper API Integration
✅ Search for latest regulatory updates  
✅ Find relevant compliance case studies  
✅ Get news about regulation changes  
✅ Verify regulatory requirements  

### Groq API Integration
✅ Ultra-fast compliance recommendations  
✅ Real-time clause generation  
✅ Enhanced risk analysis  
✅ Multi-framework comparison  

---

## 8. Usage Examples

### Reading from Google Sheets
```python
from services.google_sheets_service import GoogleSheetsService

sheets = GoogleSheetsService()
text = sheets.extract_text_from_sheet(
    url="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
    sheet_name="Contract",
    cell_range="A1:B100"
)
```

### Writing Reports to Google Sheets
```python
from services.google_sheets_writer import GoogleSheetsWriter

writer = GoogleSheetsWriter()
writer.write_compliance_report(
    spreadsheet_id="YOUR_SHEET_ID",
    report_data=compliance_results
)
```

### Searching Regulatory Updates
```python
from services.serper_service import SerperService

serper = SerperService()
results = serper.search_regulatory_updates("GDPR latest amendments 2025")
```

### Getting Groq Recommendations
```python
from services.groq_service import GroqService

groq = GroqService()
recommendation = groq.generate_compliant_clause(
    clause_type="Data Processing",
    framework="GDPR",
    context="Cloud storage provider"
)
```

---

## 9. Security Best Practices

⚠️ **IMPORTANT**: Never commit API keys or credentials to Git!

The `.gitignore` file already excludes:
- `.env`
- `config/google_credentials.json`

### Verify Protection
```powershell
git status
# Make sure .env and google_credentials.json don't appear
```

---

## 10. Troubleshooting

### Google Sheets: "Permission Denied"
**Solution**: Make sure you shared the sheet with the service account email

### Serper API: "Invalid API Key"
**Solution**: Check that you copied the complete API key without spaces

### Groq API: "Authentication Failed"
**Solution**: Make sure the key starts with `gsk_` and is complete

### Import Errors
**Solution**: 
```powershell
pip install --upgrade groq google-auth google-api-python-client requests
```

---

## Next Steps

1. ✅ Complete all API setups above
2. ✅ Run test script to verify connections
3. ✅ Try reading a contract from Google Sheets
4. ✅ Generate and export a compliance report
5. ✅ Test real-time notifications

---

## Cost Summary

| Service | Free Tier | Cost After Free |
|---------|-----------|-----------------|
| Google Sheets API | Unlimited | Free |
| Serper API | 2,500 searches | $50/month (5K) |
| Groq API | 14,400 req/day | Very generous |

**Total Setup Cost**: $0 with free tiers! 🎉

---

Ready to implement? Let's start with the code! 🚀
