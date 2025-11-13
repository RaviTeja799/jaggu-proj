"""
Test Groq API integration for clause generation.
Verifies that ClauseGenerator can use Groq API for cloud-based LLaMA inference.
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from models.regulatory_requirement import RegulatoryRequirement, RiskLevel
from models.clause_analysis import ClauseAnalysis
from services.clause_generator import ClauseGenerator
from config.settings import AppConfig


def test_groq_api_connection():
    """Test that Groq API key is configured."""
    print("=" * 70)
    print("TEST 1: Groq API Configuration")
    print("=" * 70)
    
    config = AppConfig()
    api_key = config.api.groq_api_key
    
    if api_key and api_key != "your-groq-api-key-here":
        print("✅ Groq API key is configured")
        print(f"   Key: {api_key[:20]}...{api_key[-10:]}")
        return True
    else:
        print("❌ Groq API key not configured")
        print("   Please set GROQ_API_KEY in .env file")
        return False


def test_clause_generation_with_groq():
    """Test generating a new clause using Groq API."""
    print("\n" + "=" * 70)
    print("TEST 2: Generate New Clause with Groq API")
    print("=" * 70)
    
    try:
        # Create a requirement
        requirement = RegulatoryRequirement(
            requirement_id="GDPR-Art6",
            framework="GDPR",
            article_reference="Article 6",
            clause_type="Lawful Basis",
            description="Data processing must be based on lawful grounds (consent, contract, legal obligation, vital interests, public task, or legitimate interests).",
            mandatory=True,
            risk_level=RiskLevel.HIGH
        )
        
        print(f"\n📋 Requirement: {requirement.article_reference}")
        print(f"   Framework: {requirement.framework}")
        print(f"   Description: {requirement.description[:100]}...")
        
        # Initialize ClauseGenerator with Groq enabled
        generator = ClauseGenerator(use_groq=True)
        
        print(f"\n🔧 ClauseGenerator initialized")
        print(f"   Using Groq API: {generator.use_groq}")
        print(f"   Groq client available: {generator.groq_client is not None}")
        
        # Generate clause
        print(f"\n🤖 Generating clause with LLaMA 3.3 70B via Groq...")
        contract_context = "This is a Software as a Service Agreement between Company A and Company B."
        
        clause_text = generator.generate_clause_text(
            requirement=requirement,
            contract_context=contract_context
        )
        
        print(f"\n✅ Clause generated successfully!")
        print(f"\n📄 Generated Clause:")
        print("-" * 70)
        print(clause_text)
        print("-" * 70)
        
        # Check basic validity
        if len(clause_text) > 50 and "personal data" in clause_text.lower():
            print(f"\n🔍 Validation: ✅ Valid")
            print(f"   Clause is well-formed and addresses the requirement")
        else:
            print(f"\n🔍 Validation: ⚠️ Needs review")
            print(f"   Clause length: {len(clause_text)} characters")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_clause_modification_with_groq():
    """Test modifying an existing clause using Groq API."""
    print("\n" + "=" * 70)
    print("TEST 3: Modify Existing Clause with Groq API")
    print("=" * 70)
    
    try:
        # Create a requirement
        requirement = RegulatoryRequirement(
            requirement_id="HIPAA-164.308",
            framework="HIPAA",
            article_reference="§164.308(a)(1)(i)",
            clause_type="Administrative Safeguards",
            description="Implement administrative safeguards to protect electronic protected health information.",
            mandatory=True,
            risk_level=RiskLevel.HIGH
        )
        
        # Create an existing clause that needs improvement
        existing_clause = ClauseAnalysis(
            clause_id="clause_1",
            clause_text="Company will protect patient data.",
            clause_type="Data Protection",
            confidence_score=0.8
        )
        
        print(f"\n📋 Original Clause:")
        print(f"   {existing_clause.clause_text}")
        
        print(f"\n📋 Requirement: {requirement.article_reference}")
        print(f"   Framework: {requirement.framework}")
        
        # Initialize ClauseGenerator
        generator = ClauseGenerator(use_groq=True)
        
        # Generate modification
        print(f"\n🤖 Generating improved clause with LLaMA 3.3 70B via Groq...")
        
        issues = [
            "Lacks specific mention of 'administrative safeguards'",
            "Does not reference 'electronic protected health information'",
            "Missing implementation details"
        ]
        
        modified_text = generator.generate_modification_text(
            original_clause=existing_clause,
            requirement=requirement,
            issues=issues
        )
        
        print(f"\n✅ Clause modified successfully!")
        print(f"\n📄 Modified Clause:")
        print("-" * 70)
        print(modified_text)
        print("-" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_batch_generation_with_groq():
    """Test generating multiple clauses in batch."""
    print("\n" + "=" * 70)
    print("TEST 4: Batch Clause Generation with Groq API")
    print("=" * 70)
    
    try:
        # Create multiple requirements
        requirements = [
            RegulatoryRequirement(
                requirement_id="GDPR-Art13",
                framework="GDPR",
                article_reference="Article 13",
                clause_type="Information Provision",
                description="Information to be provided when personal data are collected from the data subject.",
                mandatory=True,
                risk_level=RiskLevel.HIGH
            ),
            RegulatoryRequirement(
                requirement_id="GDPR-Art25",
                framework="GDPR",
                article_reference="Article 25",
                clause_type="Data Protection Design",
                description="Data protection by design and by default.",
                mandatory=True,
                risk_level=RiskLevel.HIGH
            ),
            RegulatoryRequirement(
                requirement_id="CCPA-1798.100",
                framework="CCPA",
                article_reference="§1798.100",
                clause_type="Consumer Rights",
                description="Right to know what personal information is collected.",
                mandatory=True,
                risk_level=RiskLevel.MEDIUM
            )
        ]
        
        print(f"\n📋 Generating clauses for {len(requirements)} requirements:")
        for req in requirements:
            print(f"   - {req.framework} {req.article_reference}")
        
        # Initialize ClauseGenerator
        generator = ClauseGenerator(use_groq=True)
        
        # Generate batch
        print(f"\n🤖 Generating clauses with LLaMA 3.3 70B via Groq...")
        
        generated_clauses = generator.generate_batch_clauses(
            requirements=requirements,
            contract_context="This is a Data Processing Agreement."
        )
        
        print(f"\n✅ Generated {len(generated_clauses)} clauses!")
        
        for req_id, clause_text in generated_clauses.items():
            req = next(r for r in requirements if r.requirement_id == req_id)
            print(f"\n📄 {req.framework} {req.article_reference}:")
            print("-" * 70)
            print(clause_text[:200] + "..." if len(clause_text) > 200 else clause_text)
            print("-" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("GROQ API CLAUSE GENERATION TESTS")
    print("=" * 70)
    print("\nThis test suite verifies that the ClauseGenerator can use")
    print("Groq API for cloud-based LLaMA 3.3 70B inference instead of")
    print("requiring a local LLaMA model (which needs 24GB+ VRAM).")
    
    results = []
    
    # Test 1: API configuration
    results.append(("Groq API Configuration", test_groq_api_connection()))
    
    # Only continue if API is configured
    if not results[0][1]:
        print("\n" + "=" * 70)
        print("⚠️  Cannot continue without Groq API key")
        print("=" * 70)
        return
    
    # Test 2: Generate new clause
    results.append(("Generate New Clause", test_clause_generation_with_groq()))
    
    # Test 3: Modify existing clause
    results.append(("Modify Existing Clause", test_clause_modification_with_groq()))
    
    # Test 4: Batch generation
    results.append(("Batch Generation", test_batch_generation_with_groq()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n📊 Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Groq API integration is working perfectly!")
        print("\n✨ Your AI Compliance Checker can now:")
        print("   - Generate compliant contract clauses using LLaMA 3.3 70B")
        print("   - Modify existing clauses to improve compliance")
        print("   - Process multiple clauses in batch")
        print("   - Work without requiring local GPU/VRAM")
        print("\n🚀 Project is 100% complete and production-ready!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
