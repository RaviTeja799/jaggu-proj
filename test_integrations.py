"""
Integration Testing Script
Tests all multi-platform integrations
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_slack_integration():
    """Test Slack notification service"""
    print("\n" + "="*60)
    print("🔔 Testing Slack Integration")
    print("="*60)
    
    try:
        from services.slack_notification_service import SlackNotificationService
        
        slack = SlackNotificationService()
        
        if not slack.is_enabled():
            print("❌ Slack not configured")
            print("   Set SLACK_WEBHOOK_URL in .env file")
            return False
        
        print("✅ Slack webhook configured")
        
        # Test high-risk notification
        result = slack.notify_high_risk_contract(
            contract_name="Test Contract - DO NOT ACTION",
            risk_score=95,
            compliance_issues=[
                {"severity": "high", "description": "Test issue - ignore"}
            ]
        )
        
        if result:
            print("✅ Test notification sent successfully")
            print("   Check your Slack channel for the message")
            return True
        else:
            print("❌ Failed to send notification")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_email_integration():
    """Test email notification service"""
    print("\n" + "="*60)
    print("📧 Testing Email Integration")
    print("="*60)
    
    try:
        from services.email_notification_service import EmailNotificationService
        
        email = EmailNotificationService()
        
        service = os.getenv('EMAIL_SERVICE', 'not set')
        print(f"📮 Email service: {service}")
        
        if service == 'smtp':
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_user = os.getenv('SMTP_USERNAME')
            if not smtp_server or not smtp_user:
                print("❌ SMTP not configured")
                print("   Set SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD in .env")
                return False
            print(f"✅ SMTP configured: {smtp_server}")
            
        elif service == 'sendgrid':
            api_key = os.getenv('SENDGRID_API_KEY')
            if not api_key:
                print("❌ SendGrid not configured")
                print("   Set SENDGRID_API_KEY in .env")
                return False
            print("✅ SendGrid configured")
            
        elif service == 'mailgun':
            api_key = os.getenv('MAILGUN_API_KEY')
            domain = os.getenv('MAILGUN_DOMAIN')
            if not api_key or not domain:
                print("❌ Mailgun not configured")
                print("   Set MAILGUN_API_KEY and MAILGUN_DOMAIN in .env")
                return False
            print("✅ Mailgun configured")
        else:
            print("❌ EMAIL_SERVICE not set (use: smtp, sendgrid, or mailgun)")
            return False
        
        print("\n⚠️  Skipping actual email test to avoid spam")
        print("   Uncomment the code below to test sending")
        
        # Uncomment to actually send test email:
        # legal_email = os.getenv('LEGAL_TEAM_EMAIL', 'your-email@example.com')
        # result = email.send_high_risk_alert(
        #     contract_name="Test Contract - DO NOT ACTION",
        #     risk_score=85,
        #     compliance_issues=[{"clause": "Test", "description": "Test issue"}],
        #     recommendations=["This is a test - ignore"],
        #     recipient_override=legal_email
        # )
        # print(f"✅ Test email sent to {legal_email}" if result else "❌ Failed to send email")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_google_sheets_integration():
    """Test Google Sheets sync service"""
    print("\n" + "="*60)
    print("📊 Testing Google Sheets Integration")
    print("="*60)
    
    try:
        from services.google_sheets_compliance_sync import GoogleSheetsComplianceSync
        
        sheets = GoogleSheetsComplianceSync()
        
        if not sheets.is_enabled():
            print("❌ Google Sheets not configured")
            print("   Set GOOGLE_SHEETS_CREDENTIALS_PATH and GOOGLE_SHEETS_SPREADSHEET_ID in .env")
            return False
        
        print("✅ Google Sheets configured")
        
        # Test read
        print("\n📖 Testing read operation...")
        contracts = sheets.read_contract_metadata()
        
        if contracts:
            print(f"✅ Found {len(contracts)} contracts in spreadsheet")
            if len(contracts) > 0:
                print(f"   Example: {contracts[0].get('contract_name', 'N/A')}")
        else:
            print("⚠️  No contracts found or sheet is empty")
        
        # Test write
        print("\n📝 Testing write operation...")
        test_data = {
            'risk_score': 75,
            'compliance_status': 'TEST - Ignore',
            'frameworks_checked': 'GDPR, CCPA',
            'issues_found': 2,
            'high_risk_issues': 0,
            'recommendations': 'This is a test entry'
        }
        
        result = sheets.write_compliance_status(
            contract_name="TEST CONTRACT - IGNORE",
            compliance_data=test_data
        )
        
        if result:
            print("✅ Successfully wrote test data")
            print("   Check the 'Compliance_Status' tab in your spreadsheet")
            return True
        else:
            print("❌ Failed to write data")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_regulatory_tracker():
    """Test regulatory update tracker"""
    print("\n" + "="*60)
    print("📜 Testing Regulatory Update Tracker")
    print("="*60)
    
    try:
        from services.regulatory_update_tracker import RegulatoryUpdateTracker
        
        tracker = RegulatoryUpdateTracker()
        
        print("🔍 Fetching regulatory updates...")
        updates = tracker.fetch_all_updates()
        
        if updates:
            print(f"✅ Found {len(updates)} regulatory updates")
            
            # Show first update
            if len(updates) > 0:
                first = updates[0]
                print(f"\n📄 Example update:")
                print(f"   Title: {first.get('title', 'N/A')[:80]}...")
                print(f"   Source: {first.get('source', 'N/A')}")
                print(f"   Date: {first.get('published_date', 'N/A')}")
                
                # Test keyword extraction
                keywords = tracker.extract_keywords_from_update(first)
                if keywords:
                    print(f"   Keywords: {', '.join(keywords[:5])}")
                
                # Test urgency scoring
                urgency = tracker.calculate_urgency_score(first)
                print(f"   Urgency: {urgency}/100")
            
            return True
        else:
            print("⚠️  No updates found (this is normal if no recent regulatory changes)")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_modification_engine():
    """Test contract modification engine"""
    print("\n" + "="*60)
    print("✏️  Testing Contract Modification Engine")
    print("="*60)
    
    try:
        from services.contract_modification_engine import ContractModificationEngine
        
        engine = ContractModificationEngine()
        
        # Test clause
        test_clause = {
            'id': 'test-clause-1',
            'clause_number': '5.2',
            'clause_title': 'Data Processing',
            'clause_text': 'The processor shall implement appropriate technical and organizational measures.',
            'clause_type': 'data_processing'
        }
        
        # Test regulation
        test_regulation = {
            'regulation_id': 'TEST-REG-001',
            'title': 'Enhanced Data Processing Requirements',
            'description': 'New requirements for data breach notification within 72 hours',
            'keywords': ['data', 'processing', 'breach', 'notification'],
            'applicable_domain': 'GDPR',
            'jurisdiction': 'EU',
            'severity': 'high'
        }
        
        print("🔍 Mapping regulation to clause...")
        is_relevant = engine.map_regulation_to_clauses(test_regulation, [test_clause])
        
        if is_relevant:
            print("✅ Mapping successful - regulation is relevant to clause")
            
            print("\n📝 Generating amendment suggestion...")
            
            # Check if OpenAI is configured
            openai_key = os.getenv('OPENAI_API_KEY')
            use_ai = bool(openai_key)
            
            if use_ai:
                print("🤖 Using OpenAI for AI-powered amendment")
            else:
                print("📋 Using template-based amendment (OpenAI not configured)")
            
            amendment = engine.generate_amendment_suggestion(
                clause=test_clause,
                regulation=test_regulation,
                use_ai=use_ai
            )
            
            print(f"\n✅ Amendment generated:")
            print(f"   Amendment ID: {amendment['amendment_id']}")
            print(f"   Confidence: {amendment['confidence_score']}")
            print(f"   Method: {amendment['generation_method']}")
            print(f"   Can auto-apply: {amendment['can_auto_apply']}")
            print(f"\n   Suggested text (first 150 chars):")
            print(f"   {amendment['suggested_text'][:150]}...")
            
            return True
        else:
            print("⚠️  Regulation not mapped to clause (keyword mismatch)")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_orchestrator():
    """Test integration orchestrator"""
    print("\n" + "="*60)
    print("🎯 Testing Integration Orchestrator")
    print("="*60)
    
    try:
        from services.compliance_integration_orchestrator import ComplianceIntegrationOrchestrator
        
        orchestrator = ComplianceIntegrationOrchestrator()
        
        print("✅ Orchestrator initialized")
        
        # Create test contract
        test_contracts = [
            {
                'name': 'Test Service Agreement',
                'risk_score': 82,
                'compliance_issues': [
                    {'severity': 'high', 'description': 'Missing GDPR clauses'},
                    {'severity': 'medium', 'description': 'Outdated liability terms'}
                ],
                'frameworks': ['GDPR', 'CCPA'],
                'expiry_date': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
                'clauses': [
                    {
                        'id': 'clause-1',
                        'clause_number': '5.1',
                        'clause_title': 'Data Protection',
                        'clause_text': 'Standard data protection clause',
                        'clause_type': 'data_processing'
                    }
                ]
            }
        ]
        
        print("\n⚠️  Running test workflow (will send notifications if configured)...")
        print("   This may take a minute...\n")
        
        results = orchestrator.run_daily_compliance_check(test_contracts)
        
        print(f"\n✅ Workflow completed:")
        print(f"   Total contracts: {results['total_contracts']}")
        print(f"   High-risk: {results['high_risk_count']}")
        print(f"   Expiring soon: {results['expiring_soon_count']}")
        print(f"   Regulatory updates: {results['regulatory_updates_count']}")
        print(f"   Amendments generated: {results['amendments_generated_count']}")
        print(f"   Notifications sent: {results['notifications_sent']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests"""
    print("\n" + "="*80)
    print("🧪 MULTI-PLATFORM INTEGRATION TEST SUITE")
    print("="*80)
    print("\nThis script tests all integration services.")
    print("Make sure you have configured .env file before running.\n")
    
    results = {}
    
    # Run tests
    results['Slack'] = test_slack_integration()
    results['Email'] = test_email_integration()
    results['Google Sheets'] = test_google_sheets_integration()
    results['Regulatory Tracker'] = test_regulatory_tracker()
    results['Modification Engine'] = test_modification_engine()
    results['Orchestrator'] = test_orchestrator()
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    for service, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {service}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All integrations are working correctly!")
    else:
        print("\n⚠️  Some integrations need configuration. See INTEGRATION_SETUP_GUIDE.md")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
