"""Test Multi-Platform Integration - Test all API connections and services."""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("MULTI-PLATFORM INTEGRATION TEST")
print("=" * 70)
print()

# Test 1: Environment Variables
print("1. Testing Environment Variables...")
print("-" * 70)

env_file = project_root / '.env'
if env_file.exists():
    print(f"✓ .env file found: {env_file}")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check required variables
    required_vars = {
        'SERPER_API_KEY': os.getenv('SERPER_API_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
    }
    
    for var_name, var_value in required_vars.items():
        if var_value:
            masked_value = var_value[:8] + '...' + var_value[-4:]
            print(f"✓ {var_name}: {masked_value}")
        else:
            print(f"✗ {var_name}: Not set")
else:
    print(f"✗ .env file not found")

print()

# Test 2: Google Sheets Service
print("2. Testing Google Sheets Service...")
print("-" * 70)

try:
    from services.google_sheets_service import GoogleSheetsService
    from services.google_sheets_writer import GoogleSheetsWriter
    
    sheets_reader = GoogleSheetsService()
    sheets_writer = GoogleSheetsWriter()
    
    print("✓ Google Sheets services imported successfully")
    
    # Check for credentials
    creds_path = project_root / 'config' / 'google_credentials.json'
    if creds_path.exists():
        print(f"✓ Google credentials found: {creds_path}")
        
        # Test connection
        if sheets_reader.test_connection():
            print("✓ Google Sheets API connection successful")
        else:
            print("✗ Google Sheets API connection failed")
    else:
        print(f"⚠ Google credentials not found: {creds_path}")
        print("  Follow the setup guide in MULTI_PLATFORM_INTEGRATION_GUIDE.md")
    
except Exception as e:
    print(f"✗ Google Sheets test failed: {e}")

print()

# Test 3: Serper API Service
print("3. Testing Serper API Service...")
print("-" * 70)

try:
    from services.serper_service import SerperService
    
    serper = SerperService()
    print("✓ Serper service imported successfully")
    
    if os.getenv('SERPER_API_KEY'):
        # Test connection
        if serper.test_connection():
            print("✓ Serper API connection successful")
            
            # Try a simple search
            print("  Testing search functionality...")
            results = serper.search("GDPR compliance", num_results=3)
            if results and 'organic' in results:
                print(f"  ✓ Search returned {len(results.get('organic', []))} results")
            else:
                print("  ⚠ Search returned unexpected format")
        else:
            print("✗ Serper API connection failed")
    else:
        print("⚠ SERPER_API_KEY not set")
        print("  Get your free API key from https://serper.dev")
    
except Exception as e:
    print(f"✗ Serper test failed: {e}")

print()

# Test 4: Groq API Service
print("4. Testing Groq API Service...")
print("-" * 70)

try:
    from services.groq_service import GroqService
    
    groq = GroqService()
    print("✓ Groq service imported successfully")
    
    if os.getenv('GROQ_API_KEY'):
        # Test connection
        if groq.test_connection():
            print("✓ Groq API connection successful")
            
            # Try generating a simple response
            print("  Testing clause generation...")
            try:
                result = groq.generate_compliant_clause(
                    clause_type="Data Processing",
                    framework="GDPR",
                    context="Cloud storage provider",
                    model="llama-3.3-70b-versatile"
                )
                if result and 'clause' in result:
                    print("  ✓ Clause generation successful")
                    print(f"  Generated {len(result['clause'])} characters")
                else:
                    print("  ⚠ Clause generation returned unexpected format")
            except Exception as e:
                print(f"  ✗ Clause generation failed: {e}")
        else:
            print("✗ Groq API connection failed")
    else:
        print("⚠ GROQ_API_KEY not set")
        print("  Get your free API key from https://console.groq.com")
    
except ImportError as e:
    print(f"✗ Groq library not installed: {e}")
    print("  Install with: pip install groq")
except Exception as e:
    print(f"✗ Groq test failed: {e}")

print()

# Test 5: Notification System
print("5. Testing Notification System...")
print("-" * 70)

try:
    from services.notification_system import NotificationSystem, NotificationType, NotificationSeverity
    
    notif_system = NotificationSystem()
    print("✓ Notification system imported successfully")
    
    # Test sending a notification
    success = notif_system.send_notification(
        notification_type=NotificationType.SYSTEM_ALERT,
        severity=NotificationSeverity.INFO,
        message="Test notification",
        details={'test': True},
        targets=['sheets']
    )
    
    if success:
        print("✓ Notification system functional")
    else:
        print("⚠ Notification sending returned False")
    
    # Get notification report
    report = notif_system.generate_notification_report()
    print(f"✓ Generated notification report: {report['total_notifications']} notifications")
    
except Exception as e:
    print(f"✗ Notification system test failed: {e}")

print()

# Test 6: Integration Test
print("6. Testing Integration Workflow...")
print("-" * 70)

try:
    print("Testing regulatory update search with notification...")
    
    if os.getenv('SERPER_API_KEY'):
        from services.serper_service import SerperService
        from services.notification_system import NotificationSystem, NotificationType, NotificationSeverity
        
        serper = SerperService()
        notif_system = NotificationSystem()
        
        # Search for GDPR updates
        updates = serper.search_regulatory_updates("GDPR", year=2025)
        
        if updates:
            print(f"✓ Found {len(updates)} regulatory updates")
            
            # Send notification for first update
            if len(updates) > 0:
                update = updates[0]
                notif_system.notify_regulatory_update(
                    framework="GDPR",
                    update_title=update.get('title', 'Unknown'),
                    update_summary=update.get('snippet', 'No summary'),
                    source=update.get('source', 'Unknown'),
                    link=update.get('link', '')
                )
                print("✓ Regulatory update notification sent")
        else:
            print("⚠ No updates found (might be API limit)")
    else:
        print("⚠ Skipping (SERPER_API_KEY not set)")
    
except Exception as e:
    print(f"✗ Integration test failed: {e}")

print()

# Summary
print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)

print("\nSetup Checklist:")
print("  [ ] Install dependencies: pip install groq python-dotenv requests")
print("  [ ] Set up Google Sheets API (see MULTI_PLATFORM_INTEGRATION_GUIDE.md)")
print("  [ ] Get Serper API key from https://serper.dev")
print("  [ ] Get Groq API key from https://console.groq.com")
print("  [ ] Add API keys to .env file")
print()

print("Next Steps:")
print("  1. Complete any missing setups from the checklist above")
print("  2. Run this test again to verify all connections")
print("  3. Try the example workflows in the integration guide")
print("  4. Start using multi-platform features in your application")
print()

print("Documentation:")
print("  - Setup Guide: MULTI_PLATFORM_INTEGRATION_GUIDE.md")
print("  - Google Sheets: config/GOOGLE_SHEETS_SETUP.md")
print()

print("=" * 70)
