"""
Google Service Account Setup Helper

IMPORTANT: You have OAuth credentials, but we need Service Account credentials!

This script will guide you through creating proper Service Account credentials
for Google Sheets integration.
"""

import json
from pathlib import Path

print("="*70)
print("GOOGLE SHEETS CREDENTIALS SETUP")
print("="*70)
print()

# Check what credentials we have
oauth_creds = Path(__file__).parent / 'config' / 'google_oauth_credentials.json'
service_creds = Path(__file__).parent / 'config' / 'google_credentials.json'

print("📋 Current Status:")
print(f"  OAuth Credentials: {'✓ Found' if oauth_creds.exists() else '✗ Not found'}")
print(f"  Service Account Credentials: {'✓ Found' if service_creds.exists() else '✗ Not found'}")
print()

if oauth_creds.exists():
    with open(oauth_creds, 'r') as f:
        oauth_data = json.load(f)
    
    print("⚠️  ISSUE DETECTED:")
    print("  You have OAuth credentials (for web apps with user login),")
    print("  but we need Service Account credentials (for server-side access).")
    print()

print("="*70)
print("HOW TO CREATE SERVICE ACCOUNT CREDENTIALS")
print("="*70)
print()

print("Follow these steps to create Service Account credentials:")
print()

print("1️⃣  Go to Google Cloud Console")
print("   URL: https://console.cloud.google.com")
print()

if oauth_creds.exists():
    print(f"2️⃣  Select your project: {oauth_data.get('web', {}).get('project_id', 'your-project')}")
else:
    print("2️⃣  Select your project or create a new one")
print()

print("3️⃣  Enable APIs")
print("   - Go to: APIs & Services → Library")
print("   - Search and enable: 'Google Sheets API'")
print("   - Search and enable: 'Google Drive API'")
print()

print("4️⃣  Create Service Account")
print("   - Go to: APIs & Services → Credentials")
print("   - Click: CREATE CREDENTIALS → Service Account")
print("   - Name: compliance-checker-service")
print("   - Click: CREATE AND CONTINUE")
print("   - Skip optional steps → DONE")
print()

print("5️⃣  Generate JSON Key")
print("   - Click on the service account you just created")
print("   - Go to: KEYS tab")
print("   - Click: ADD KEY → Create new key")
print("   - Choose: JSON")
print("   - Click: CREATE")
print("   - File will download automatically")
print()

print("6️⃣  Install the Key")
config_dir = Path(__file__).parent / 'config'
print(f"   - Rename the downloaded file to: google_credentials.json")
print(f"   - Move it to: {config_dir.absolute()}")
print()

print("7️⃣  Get Service Account Email")
print("   - Open the downloaded JSON file")
print("   - Find the 'client_email' field")
print("   - It will look like: your-service@project-id.iam.gserviceaccount.com")
print("   - Copy this email!")
print()

print("8️⃣  Share Your Google Sheets")
print("   - Open any Google Sheet you want to use")
print("   - Click: Share button")
print("   - Paste the service account email")
print("   - Set permission: Editor (for writing) or Viewer (for reading)")
print("   - Uncheck: Notify people")
print("   - Click: Share")
print()

print("="*70)
print("ALTERNATIVE: Quick Setup Script")
print("="*70)
print()
print("If you already have a service account JSON file downloaded:")
print()
print("  PowerShell:")
print(f'  Copy-Item "Downloads\\your-service-account-file.json" "{config_dir.absolute()}\\google_credentials.json"')
print()
print("After copying, run the test:")
print("  python test_multi_platform_integration.py")
print()

print("="*70)
print("NEED HELP?")
print("="*70)
print()
print("Full guide: MULTI_PLATFORM_INTEGRATION_GUIDE.md")
print("Quick ref: API_QUICK_REFERENCE.md")
print()

# Offer to open browser
print("Would you like to open Google Cloud Console now? (y/n): ", end="")
try:
    choice = input().strip().lower()
    if choice == 'y':
        import webbrowser
        webbrowser.open('https://console.cloud.google.com/apis/credentials')
        print("\n✓ Opening Google Cloud Console in your browser...")
except:
    pass

print()
print("="*70)
