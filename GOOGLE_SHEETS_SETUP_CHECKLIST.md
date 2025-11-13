# ✅ Google Sheets Setup - Simple Checklist

## 📝 Follow These Steps (10 Minutes)

### Step 1: Open Google Cloud Console
- URL: https://console.cloud.google.com
- Select project: **august-will-477705-i7**

---

### Step 2: Enable APIs (2 minutes)
1. Click **APIs & Services** (left sidebar)
2. Click **Library**
3. Search for: `Google Sheets API`
   - Click it → Click **ENABLE**
4. Search for: `Google Drive API`
   - Click it → Click **ENABLE**

---

### Step 3: Create Service Account (3 minutes)
1. Click **APIs & Services** → **Credentials**
2. Click **CREATE CREDENTIALS** (blue button at top)
3. Select **Service Account**
4. Fill in:
   - **Service account name**: `compliance-checker-service`
   - **Description**: `For AI Compliance Checker app`
5. Click **CREATE AND CONTINUE**
6. **Skip** the optional roles section
7. Click **DONE**

---

### Step 4: Download JSON Key (1 minute)
1. You'll see your new service account in the list
2. Click on it (click the email address)
3. Go to **KEYS** tab (top of page)
4. Click **ADD KEY** → **Create new key**
5. Choose **JSON** format
6. Click **CREATE**
7. File downloads automatically (looks like: `august-will-477705-i7-xxxxx.json`)

---

### Step 5: Install the Key File (1 minute)
**Option A - Copy via File Explorer:**
1. Find the downloaded JSON file in your Downloads folder
2. Rename it to: `google_credentials.json`
3. Copy it to: `E:\323103310024\Updated Infosys\jaggu-proj\config\`

**Option B - Copy via PowerShell:**
```powershell
# Replace "Downloads\august-will-xxxxx.json" with your actual filename
Copy-Item "$env:USERPROFILE\Downloads\august-will-477705-*.json" "E:\323103310024\Updated Infosys\jaggu-proj\config\google_credentials.json"
```

---

### Step 6: Get Service Account Email (1 minute)
1. Open the JSON file you just copied (with Notepad)
2. Find the line with `"client_email"`
3. Copy the email (looks like: `compliance-checker-service@august-will-477705-i7.iam.gserviceaccount.com`)

---

### Step 7: Share Your Google Sheet (2 minutes)
1. Open any Google Sheet you want to use with the app
2. Click **Share** button (top right)
3. Paste the service account email
4. Set permission to **Editor**
5. **Uncheck** "Notify people"
6. Click **Share**

---

### Step 8: Test It! (1 minute)
Run this command to verify everything works:

```powershell
python test_multi_platform_integration.py
```

✅ If you see "Google Sheets: Connected ✓" - You're done!

---

## 🎯 Quick Reference

### What You Need:
- ✅ Google Cloud project: `august-will-477705-i7`
- ✅ APIs enabled: Google Sheets API + Google Drive API
- ✅ Service account created
- ✅ JSON key file saved as: `config/google_credentials.json`
- ✅ Google Sheet shared with service account email

### File Location:
```
E:\323103310024\Updated Infosys\jaggu-proj\config\google_credentials.json
```

### Service Account Email Format:
```
compliance-checker-service@august-will-477705-i7.iam.gserviceaccount.com
```

---

## ⚠️ Common Issues

### "Credentials file not found"
→ Make sure file is named exactly: `google_credentials.json`
→ Make sure it's in the `config/` folder

### "Permission denied" when accessing sheet
→ Make sure you shared the sheet with the service account email
→ Make sure you set permission to "Editor" (not "Viewer")

### "API not enabled"
→ Go back to Google Cloud Console → APIs & Services → Library
→ Make sure both Google Sheets API and Google Drive API show "ENABLED"

---

## 🎉 What You Can Do After Setup

Once setup is complete, your app can:

✅ **Read** contracts from Google Sheets
✅ **Write** compliance reports to new sheets
✅ **Export** analysis results automatically
✅ **Log** notifications and alerts

---

## 📚 Example Usage

```python
from services.google_sheets_service import GoogleSheetsService
from services.google_sheets_writer import GoogleSheetsWriter

# Read contracts
reader = GoogleSheetsService()
contracts = reader.read_contracts_from_sheet(
    sheet_url="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"
)

# Write results
writer = GoogleSheetsWriter()
writer.write_compliance_report(
    data=your_analysis_results,
    sheet_name="Compliance Report"
)
```

---

## 🔗 Helpful Links

- Google Cloud Console: https://console.cloud.google.com
- Your Project: https://console.cloud.google.com/apis/credentials?project=august-will-477705-i7
- Enable APIs: https://console.cloud.google.com/apis/library?project=august-will-477705-i7

---

**Need Help?** Check `MULTI_PLATFORM_INTEGRATION_GUIDE.md` for detailed instructions.
