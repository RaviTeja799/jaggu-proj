"""Example usage of Multi-Platform Integration features."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Example 1: Reading Contract from Google Sheets and Analyzing
def example_google_sheets_analysis():
    """Example: Read a contract from Google Sheets and analyze it."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Google Sheets Contract Analysis")
    print("="*70)
    
    from services.google_sheets_service import GoogleSheetsService
    from services.document_processor import DocumentProcessor
    from services.nlp_analyzer import NLPAnalyzer
    from services.compliance_checker import ComplianceChecker
    
    # Initialize services
    sheets_service = GoogleSheetsService()
    doc_processor = DocumentProcessor()
    nlp_analyzer = NLPAnalyzer()
    compliance_checker = ComplianceChecker()
    
    # Example Google Sheets URL (replace with your own)
    sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
    
    try:
        # Step 1: Extract text from Google Sheets
        print("\n1. Extracting contract text from Google Sheets...")
        contract_text = sheets_service.extract_text_from_sheet(
            url=sheet_url,
            sheet_name="Contract",  # Optional
            cell_range="A1:B100"    # Optional
        )
        print(f"✓ Extracted {len(contract_text)} characters")
        
        # Step 2: Process document
        print("\n2. Processing document...")
        processed_doc = doc_processor.process_text(contract_text, "Contract from Google Sheets")
        print(f"✓ Processed document: {processed_doc.doc_id}")
        
        # Step 3: Analyze clauses
        print("\n3. Analyzing clauses with NLP...")
        clauses = nlp_analyzer.analyze_clauses(processed_doc.text)
        print(f"✓ Identified {len(clauses)} clauses")
        
        # Step 4: Check compliance
        print("\n4. Checking compliance...")
        frameworks = ["GDPR", "HIPAA"]
        results = compliance_checker.check_compliance(clauses, frameworks)
        print(f"✓ Compliance score: {results['overall_score']:.1f}%")
        
        return results
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nNote: Make sure to:")
        print("  1. Replace 'YOUR_SHEET_ID' with your actual Google Sheets ID")
        print("  2. Share the sheet with your service account email")
        print("  3. Have google_credentials.json in the config folder")
        return None


# Example 2: Writing Compliance Report to Google Sheets
def example_write_report_to_sheets():
    """Example: Write compliance analysis report to Google Sheets."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Write Compliance Report to Google Sheets")
    print("="*70)
    
    from services.google_sheets_writer import GoogleSheetsWriter
    
    writer = GoogleSheetsWriter()
    
    # Sample report data (replace with actual analysis results)
    report_data = {
        'overall_score': 78.5,
        'total_clauses': 15,
        'compliant_count': 12,
        'non_compliant_count': 3,
        'high_risk_count': 2,
        'framework_scores': {
            'GDPR': 82.3,
            'HIPAA': 74.7
        },
        'clauses': [
            {
                'id': 'clause_001',
                'type': 'Data Processing',
                'risk_level': 'Medium',
                'status': 'Compliant',
                'frameworks': ['GDPR'],
                'issues': [],
                'recommendations': []
            },
            {
                'id': 'clause_002',
                'type': 'Security',
                'risk_level': 'High',
                'status': 'Non-Compliant',
                'frameworks': ['GDPR', 'HIPAA'],
                'issues': ['Insufficient encryption requirements'],
                'recommendations': ['Add AES-256 encryption specification']
            }
        ]
    }
    
    try:
        # Option 1: Create new spreadsheet
        print("\nCreating new spreadsheet...")
        spreadsheet_id = writer.create_new_spreadsheet("Compliance Report - 2025-11-09")
        print(f"✓ Created spreadsheet: {spreadsheet_id}")
        print(f"  View at: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        
        # Write report
        print("\nWriting compliance report...")
        writer.write_compliance_report(spreadsheet_id, report_data)
        print("✓ Report written successfully")
        
        # Option 2: Write to existing spreadsheet (uncomment to use)
        # existing_sheet_id = "YOUR_EXISTING_SHEET_ID"
        # writer.write_compliance_report(existing_sheet_id, report_data, sheet_name="Analysis Results")
        
        return spreadsheet_id
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


# Example 3: Search Regulatory Updates
def example_search_regulatory_updates():
    """Example: Search for latest regulatory updates."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Search Regulatory Updates with Serper API")
    print("="*70)
    
    from services.serper_service import SerperService
    import os
    
    if not os.getenv('SERPER_API_KEY'):
        print("⚠ SERPER_API_KEY not set in .env file")
        print("  Get your free API key from https://serper.dev")
        return
    
    serper = SerperService()
    
    try:
        # Search for GDPR updates
        print("\nSearching for GDPR updates...")
        updates = serper.search_regulatory_updates("GDPR", year=2025)
        
        print(f"✓ Found {len(updates)} updates")
        
        # Display top 3
        for i, update in enumerate(updates[:3], 1):
            print(f"\n{i}. {update.get('title', 'No title')}")
            print(f"   Source: {update.get('source', 'Unknown')}")
            print(f"   Date: {update.get('date', 'N/A')}")
            print(f"   Link: {update.get('link', 'N/A')}")
            print(f"   Snippet: {update.get('snippet', 'No snippet')[:100]}...")
        
        return updates
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


# Example 4: Generate Compliant Clause with Groq
def example_generate_clause_with_groq():
    """Example: Generate compliant clause using Groq AI."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Generate Compliant Clause with Groq API")
    print("="*70)
    
    from services.groq_service import GroqService
    import os
    
    if not os.getenv('GROQ_API_KEY'):
        print("⚠ GROQ_API_KEY not set in .env file")
        print("  Get your free API key from https://console.groq.com")
        return
    
    groq = GroqService()
    
    try:
        print("\nGenerating Data Processing clause for GDPR...")
        
        result = groq.generate_compliant_clause(
            clause_type="Data Processing",
            framework="GDPR",
            context="Cloud storage provider processing customer data in EU",
            issues=[
                "Missing specification of data processing purposes",
                "No mention of data subject rights"
            ],
            model="llama-3.3-70b-versatile"
        )
        
        print("\n✓ Generated Clause:")
        print("-" * 70)
        print(result.get('clause', 'No clause generated'))
        
        print("\n✓ Explanation:")
        print("-" * 70)
        print(result.get('explanation', 'No explanation provided'))
        
        if 'key_points' in result:
            print("\n✓ Key Compliance Points:")
            for point in result['key_points']:
                print(f"  • {point}")
        
        return result
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


# Example 5: Complete Integration Workflow
def example_complete_workflow():
    """Example: Complete workflow with all integrations."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Complete Multi-Platform Integration Workflow")
    print("="*70)
    
    from services.notification_system import NotificationSystem, NotificationType, NotificationSeverity
    import os
    
    notif_system = NotificationSystem()
    
    print("\n1. Searching for regulatory updates...")
    if os.getenv('SERPER_API_KEY'):
        from services.serper_service import SerperService
        serper = SerperService()
        updates = serper.search_regulatory_updates("GDPR", year=2025)
        
        if updates and len(updates) > 0:
            print(f"✓ Found {len(updates)} updates")
            
            # Send notification for first update
            update = updates[0]
            notif_system.notify_regulatory_update(
                framework="GDPR",
                update_title=update.get('title', 'Update'),
                update_summary=update.get('snippet', 'No summary'),
                source=update.get('source', 'Unknown'),
                link=update.get('link', '')
            )
            print("✓ Notification sent for regulatory update")
    else:
        print("⚠ Skipping (SERPER_API_KEY not set)")
    
    print("\n2. Analyzing sample clause with Groq...")
    if os.getenv('GROQ_API_KEY'):
        from services.groq_service import GroqService
        groq = GroqService()
        
        sample_clause = "The company will process personal data as needed for business operations."
        
        analysis = groq.analyze_compliance_risk(sample_clause, "GDPR")
        print(f"✓ Risk Level: {analysis.get('risk_level', 'unknown')}")
        print(f"✓ Compliant: {analysis.get('compliant', False)}")
        
        if analysis.get('risk_level') == 'high':
            notif_system.notify_high_risk_clause(
                clause_id="sample_001",
                clause_text=sample_clause,
                risk_level="high",
                frameworks=["GDPR"],
                issues=analysis.get('issues', [])
            )
            print("✓ High-risk notification sent")
    else:
        print("⚠ Skipping (GROQ_API_KEY not set)")
    
    print("\n3. Generating notification report...")
    report = notif_system.generate_notification_report()
    print(f"✓ Total notifications: {report['total_notifications']}")
    print(f"✓ By severity: {report['by_severity']}")
    print(f"✓ By type: {report['by_type']}")
    
    print("\n✓ Complete workflow executed successfully")


# Main menu
def main():
    """Main menu for examples."""
    print("="*70)
    print("MULTI-PLATFORM INTEGRATION - EXAMPLE USAGE")
    print("="*70)
    print("\nAvailable Examples:")
    print("  1. Google Sheets Contract Analysis")
    print("  2. Write Compliance Report to Google Sheets")
    print("  3. Search Regulatory Updates (Serper API)")
    print("  4. Generate Compliant Clause (Groq API)")
    print("  5. Complete Integration Workflow")
    print("  0. Run All Examples")
    print()
    
    # Check setup status
    import os
    print("Current Setup Status:")
    print(f"  SERPER_API_KEY: {'✓ Set' if os.getenv('SERPER_API_KEY') else '✗ Not set'}")
    print(f"  GROQ_API_KEY: {'✓ Set' if os.getenv('GROQ_API_KEY') else '✗ Not set'}")
    
    from pathlib import Path
    creds_path = Path(__file__).parent / 'config' / 'google_credentials.json'
    print(f"  Google Credentials: {'✓ Found' if creds_path.exists() else '✗ Not found'}")
    print()
    
    choice = input("Select an example (0-5) or 'q' to quit: ").strip()
    
    if choice == '0':
        example_google_sheets_analysis()
        example_write_report_to_sheets()
        example_search_regulatory_updates()
        example_generate_clause_with_groq()
        example_complete_workflow()
    elif choice == '1':
        example_google_sheets_analysis()
    elif choice == '2':
        example_write_report_to_sheets()
    elif choice == '3':
        example_search_regulatory_updates()
    elif choice == '4':
        example_generate_clause_with_groq()
    elif choice == '5':
        example_complete_workflow()
    elif choice.lower() == 'q':
        print("Goodbye!")
        return
    else:
        print("Invalid choice")
    
    print("\n" + "="*70)
    print("For full setup instructions, see: MULTI_PLATFORM_INTEGRATION_GUIDE.md")
    print("="*70)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables
    
    main()
