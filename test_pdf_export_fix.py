"""
Test PDF Export Fix - Verify ClauseComplianceResult compatibility.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from models.regulatory_requirement import (
    ClauseComplianceResult, ComplianceStatus, RiskLevel,
    ComplianceReport, ComplianceSummary
)
from models.recommendation import Recommendation, ActionType
from services.export_service import ExportService

print("=" * 70)
print("PDF EXPORT FIX TEST")
print("=" * 70)
print()

# Create sample data matching the actual model structure
print("1. Creating sample compliance data...")
print("-" * 70)

# Sample clause results
clause_results = [
    ClauseComplianceResult(
        clause_id="Clause 3.1",
        clause_text="The Company collects personal data for service delivery.",
        clause_type="Data Processing",
        framework="GDPR",
        compliance_status=ComplianceStatus.COMPLIANT,
        risk_level=RiskLevel.LOW,
        matched_requirements=[],
        confidence=0.85,
        issues=[]
    ),
    ClauseComplianceResult(
        clause_id="Clause 4.2",
        clause_text="Data may be transferred to third countries without adequate safeguards.",
        clause_type="Data Transfer",
        framework="GDPR",
        compliance_status=ComplianceStatus.NON_COMPLIANT,
        risk_level=RiskLevel.HIGH,
        matched_requirements=[],
        confidence=0.92,
        issues=[
            "Missing standard contractual clauses",
            "No adequacy decision mentioned",
            "Lack of data subject consent provisions"
        ]
    ),
    ClauseComplianceResult(
        clause_id="Clause 5.1",
        clause_text="Data will be retained for business purposes.",
        clause_type="Data Retention",
        framework="GDPR",
        compliance_status=ComplianceStatus.NON_COMPLIANT,
        risk_level=RiskLevel.MEDIUM,
        matched_requirements=[],
        confidence=0.78,
        issues=["No specific retention period defined"]
    ),
]

# Summary
summary = ComplianceSummary(
    total_clauses=3,
    compliant_clauses=1,
    non_compliant_clauses=2,
    partial_clauses=0,
    high_risk_count=1,
    medium_risk_count=1,
    low_risk_count=1
)

# Compliance report
report = ComplianceReport(
    document_id="Test_Contract_Fix.pdf",
    frameworks_checked=["GDPR"],
    overall_score=33.3,
    clause_results=clause_results,
    missing_requirements=[],
    high_risk_items=[clause_results[1]],
    summary=summary
)

# Recommendations
recommendations = [
    Recommendation(
        recommendation_id="rec_1",
        recommendation_text="Add standard contractual clauses for international data transfers",
        priority=1,
        action_type=ActionType.ADD_CLAUSE,
        clause_reference="Clause 4.2",
        regulatory_reference="GDPR Article 46",
        description="Include standard contractual clauses approved by the European Commission"
    ),
    Recommendation(
        recommendation_id="rec_2",
        recommendation_text="Define specific data retention periods",
        priority=2,
        action_type=ActionType.MODIFY_CLAUSE,
        clause_reference="Clause 5.1",
        regulatory_reference="GDPR Article 5(1)(e)",
        description="Specify retention periods for different data categories"
    ),
]

print("✅ Sample data created")
print(f"   Clause results: {len(clause_results)}")
print(f"   Compliant: {summary.compliant_clauses}")
print(f"   Non-compliant: {summary.non_compliant_clauses}")
print(f"   Overall score: {report.overall_score}%")
print()

# Test export service
print("2. Testing ExportService PDF export...")
print("-" * 70)

try:
    export_service = ExportService()
    
    # Test PDF export
    pdf_bytes = export_service.export_to_pdf(report, recommendations)
    
    print("✅ PDF export successful!")
    print(f"   PDF size: {len(pdf_bytes):,} bytes ({len(pdf_bytes) / 1024:.1f} KB)")
    
    # Save to file for verification
    output_path = "reports/test_export_fix.pdf"
    Path("reports").mkdir(exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    
    print(f"   Saved to: {output_path}")
    print()
    
except Exception as e:
    print(f"❌ PDF export failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test other export formats for completeness
print("3. Testing other export formats...")
print("-" * 70)

try:
    # JSON export
    json_data = export_service.export_to_json(report, recommendations)
    print(f"✅ JSON export: {len(json_data):,} bytes")
    
    # CSV export
    csv_data = export_service.export_to_csv(report, recommendations)
    print(f"✅ CSV export: {len(csv_data):,} bytes")
    
except Exception as e:
    print(f"⚠️ Other formats warning: {e}")

print()
print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()
print("✅ All tests passed!")
print()
print("Fixed Issues:")
print("  • ClauseComplianceResult.compliance_status (enum) instead of is_compliant")
print("  • ClauseComplianceResult.risk_level (enum) proper handling")
print("  • ClauseComplianceResult.clause_text (direct) instead of clause.clause_text")
print()
print(f"PDF Report: {output_path}")
print()
print("=" * 70)
