"""
Verification script for PDF export fixes.
Run this to confirm all attribute accesses are correct.
"""

import sys
from models.regulatory_requirement import ClauseComplianceResult, ComplianceStatus, RiskLevel
from models.recommendation import Recommendation, ActionType
from models.regulatory_requirement import RegulatoryRequirement
from models.clause import Clause

def test_clause_compliance_result():
    """Test ClauseComplianceResult attributes"""
    print("Testing ClauseComplianceResult...")
    
    # Create a sample ClauseComplianceResult
    result = ClauseComplianceResult(
        clause_id="test_1",
        clause_text="Test clause text",
        clause_type="Data Processing",
        framework="GDPR",
        compliance_status=ComplianceStatus.COMPLIANT,
        risk_level=RiskLevel.HIGH,
        matched_requirements=[],
        confidence=0.95,
        issues=[]
    )
    
    # Verify attributes exist
    assert hasattr(result, 'compliance_status'), "❌ Missing compliance_status"
    assert hasattr(result, 'risk_level'), "❌ Missing risk_level"
    assert hasattr(result, 'clause_text'), "❌ Missing clause_text"
    
    # Verify attribute types
    assert isinstance(result.compliance_status, ComplianceStatus), "❌ compliance_status not ComplianceStatus enum"
    assert isinstance(result.risk_level, RiskLevel), "❌ risk_level not RiskLevel enum"
    assert isinstance(result.clause_text, str), "❌ clause_text not string"
    
    # Verify enum comparisons work
    assert result.compliance_status == ComplianceStatus.COMPLIANT, "❌ Enum comparison failed"
    assert result.risk_level == RiskLevel.HIGH, "❌ Risk level enum comparison failed"
    
    print("✅ ClauseComplianceResult - All tests passed!")
    return True

def test_recommendation():
    """Test Recommendation attributes"""
    print("\nTesting Recommendation...")
    
    # Create a sample requirement
    req = RegulatoryRequirement(
        requirement_id="test_req",
        framework="GDPR",
        article_reference="GDPR Article 28",
        clause_type="Data Processing",
        description="Test description",
        mandatory=True
    )
    
    # Create a sample Recommendation
    rec = Recommendation(
        recommendation_id="test_rec_1",
        requirement=req,
        priority=1,
        action_type=ActionType.ADD_CLAUSE,
        description="Test recommendation description",
        rationale="Test rationale",
        regulatory_reference="GDPR Article 28"
    )
    
    # Verify attributes exist
    assert hasattr(rec, 'description'), "❌ Missing description attribute"
    assert not hasattr(rec, 'recommendation_text'), "❌ Still has old recommendation_text attribute"
    
    # Verify attribute type
    assert isinstance(rec.description, str), "❌ description not string"
    
    # Verify content
    assert rec.description == "Test recommendation description", "❌ Description content mismatch"
    
    print("✅ Recommendation - All tests passed!")
    return True

def test_export_service_import():
    """Test that export_service imports correctly"""
    print("\nTesting ExportService import...")
    
    try:
        from services.export_service import ExportService
        print("✅ ExportService imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import ExportService: {e}")
        return False

def main():
    """Run all verification tests"""
    print("=" * 60)
    print("PDF Export Fix Verification")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(("ClauseComplianceResult", test_clause_compliance_result()))
    except Exception as e:
        print(f"❌ ClauseComplianceResult test failed: {e}")
        results.append(("ClauseComplianceResult", False))
    
    try:
        results.append(("Recommendation", test_recommendation()))
    except Exception as e:
        print(f"❌ Recommendation test failed: {e}")
        results.append(("Recommendation", False))
    
    try:
        results.append(("ExportService", test_export_service_import()))
    except Exception as e:
        print(f"❌ ExportService test failed: {e}")
        results.append(("ExportService", False))
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = all(result[1] for result in results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    
    if all_passed:
        print("✅ ALL TESTS PASSED - PDF export should work correctly!")
        print("\nNext steps:")
        print("1. Clear Python cache:")
        print("   Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Recurse -Force")
        print("2. Restart Streamlit:")
        print("   streamlit run app.py")
        print("3. Test PDF export in the web interface")
        return 0
    else:
        print("❌ SOME TESTS FAILED - Review errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
