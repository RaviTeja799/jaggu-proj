"""
Test Slack Integration - Verify Slack notifications are working.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from services.slack_notifier import SlackNotifier

print("=" * 70)
print("SLACK INTEGRATION TEST")
print("=" * 70)
print()

# Initialize Slack notifier
print("1. Initializing Slack notifier...")
print("-" * 70)
slack = SlackNotifier(default_channel="#general")

if not slack.enabled:
    print("❌ Slack notifier not enabled")
    print("\nPossible reasons:")
    print("  1. SLACK_ACCESS_TOKEN not set in .env")
    print("  2. slack-sdk not installed (run: pip install slack-sdk)")
    print("  3. Invalid access token")
    sys.exit(1)

print(f"✅ Slack notifier initialized")
print(f"   Team: {slack.team_name}")
print(f"   Bot User ID: {slack.bot_user_id}")
print()

# Test connection
print("2. Testing Slack connection...")
print("-" * 70)
if slack.test_connection():
    print("✅ Connection successful!")
else:
    print("❌ Connection failed")
    sys.exit(1)
print()

# Test 1: High-Risk Clause Alert
print("3. Testing High-Risk Clause Alert...")
print("-" * 70)
success = slack.notify_high_risk_clause(
    contract_name="Sample_Contract_2025.pdf",
    clause_id="Clause 4.2",
    clause_text="Data may be transferred to third countries without adequate safeguards or data subject consent.",
    risk_level="high",
    framework="GDPR",
    issues=[
        "Missing standard contractual clauses",
        "No adequacy decision mentioned",
        "Lack of data subject consent provisions"
    ]
)

if success:
    print("✅ High-risk clause alert sent successfully!")
else:
    print("⚠️ Failed to send alert (check channel permissions)")
print()

# Test 2: Analysis Complete Notification
print("4. Testing Analysis Complete Notification...")
print("-" * 70)
success = slack.notify_analysis_complete(
    contract_name="Test_Contract_Analysis.pdf",
    compliance_score=72.5,
    framework="GDPR",
    missing_clauses_count=8,
    high_risk_issues=3,
    processing_time=5.2
)

if success:
    print("✅ Analysis complete notification sent!")
else:
    print("⚠️ Failed to send notification")
print()

# Test 3: Batch Processing Complete
print("5. Testing Batch Processing Notification...")
print("-" * 70)
success = slack.notify_batch_complete(
    total_files=10,
    successful=9,
    failed=1,
    total_time=45.3,
    avg_compliance_score=78.4,
    high_risk_count=5
)

if success:
    print("✅ Batch processing notification sent!")
else:
    print("⚠️ Failed to send notification")
print()

# Test 4: Regulatory Update
print("6. Testing Regulatory Update Notification...")
print("-" * 70)
success = slack.notify_regulatory_update(
    framework="GDPR",
    update_title="New GDPR Guidelines on AI Systems",
    update_summary="The European Data Protection Board has issued new guidelines regarding the use of AI systems in automated decision-making processes.",
    source="EDPB",
    link="https://edpb.europa.eu/news"
)

if success:
    print("✅ Regulatory update notification sent!")
else:
    print("⚠️ Failed to send notification")
print()

# Test 5: Missing Requirements Alert
print("7. Testing Missing Requirements Alert...")
print("-" * 70)
missing_reqs = [
    {
        "requirement_name": "Data Transfer Mechanism",
        "risk_level": "high",
        "description": "No standard contractual clauses found"
    },
    {
        "requirement_name": "Breach Notification Procedure",
        "risk_level": "high",
        "description": "Missing 72-hour notification requirement"
    },
    {
        "requirement_name": "Data Subject Rights",
        "risk_level": "medium",
        "description": "Right to erasure not clearly defined"
    }
]

success = slack.notify_missing_requirements(
    contract_name="Incomplete_Contract.pdf",
    framework="GDPR",
    missing_requirements=missing_reqs
)

if success:
    print("✅ Missing requirements alert sent!")
else:
    print("⚠️ Failed to send notification")
print()

print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()
print("✅ All tests completed!")
print()
print("Check your Slack channel (#general) for the test notifications.")
print()
print("To customize:")
print("  - Change default channel in SlackNotifier initialization")
print("  - Set channel parameter in notify_* methods")
print("  - Configure different channels for different alert types")
print()
print("=" * 70)
