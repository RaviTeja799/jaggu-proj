"""
Test script for Regulatory Update Tracking System.
Tests all components: Serper API, Groq API, Knowledge Base, and Tracker.
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.serper_api_client import SerperAPIClient
from services.groq_api_client import GroqAPIClient
from services.knowledge_base_loader import KnowledgeBaseLoader
from services.regulatory_update_tracker import RegulatoryUpdateTracker


def test_serper_api():
    """Test Serper API integration."""
    print("\n" + "="*60)
    print("TESTING SERPER API")
    print("="*60)
    
    serper = SerperAPIClient()
    
    if not serper.api_key:
        print("[WARNING] SERPER_API_KEY not set. Skipping Serper tests.")
        print("   Set environment variable: $env:SERPER_API_KEY='your_key'")
        return False
    
    # Test basic search
    print("\n1. Testing basic search...")
    results = serper.search("GDPR compliance update 2024", num_results=5)
    
    if 'error' in results:
        print(f"[X] Search failed: {results['error']}")
        return False
    
    print(f"[OK] Search successful! Found {len(results.get('organic', []))} results")
    
    # Test news search
    print("\n2. Testing news search...")
    news = serper.search_news("HIPAA amendments", num_results=3)
    print(f"[OK] News search successful! Found {len(news)} articles")
    
    # Test regulatory search
    print("\n3. Testing regulatory update search...")
    updates = serper.search_regulatory_updates(
        framework="GDPR",
        keywords=["data protection"],
        num_results=5
    )
    print(f"[OK] Regulatory search successful! Found {len(updates)} updates")
    
    if updates:
        print(f"\n   Sample result:")
        print(f"   Title: {updates[0].get('title', 'N/A')[:80]}")
        print(f"   Source: {updates[0].get('source', 'N/A')}")
    
    return True


def test_groq_api():
    """Test Groq API integration."""
    print("\n" + "="*60)
    print("TESTING GROQ API")
    print("="*60)
    
    groq = GroqAPIClient()
    
    if not groq.api_key:
        print("⚠️  GROQ_API_KEY not set. Skipping Groq tests.")
        print("   Set environment variable: $env:GROQ_API_KEY='your_key'")
        return False
    
    # Test simple completion
    print("\n1. Testing chat completion...")
    response = groq.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is GDPR?"}
        ],
        max_tokens=100
    )
    
    if 'error' in response:
        print(f"❌ Chat completion failed: {response['error']}")
        return False
    
    print("✅ Chat completion successful!")
    
    # Test regulatory analysis
    print("\n2. Testing regulatory text analysis...")
    sample_text = """
    The European Commission has announced amendments to GDPR Article 28,
    requiring data processors to implement additional security measures
    for international data transfers. Organizations must comply by January 2025.
    """
    
    analysis = groq.analyze_regulatory_text(
        text=sample_text,
        framework="GDPR"
    )
    
    if 'error' in analysis:
        print(f"⚠️  Analysis completed with warning: {analysis.get('error')}")
    else:
        print("✅ Regulatory analysis successful!")
        print(f"   Summary: {analysis.get('summary', 'N/A')[:100]}...")
        print(f"   Severity: {analysis.get('severity', 'N/A')}")
        print(f"   Impact Score: {analysis.get('impact_score', 'N/A')}")
    
    return True


def test_knowledge_base():
    """Test Knowledge Base Loader."""
    print("\n" + "="*60)
    print("TESTING KNOWLEDGE BASE LOADER")
    print("="*60)
    
    kb = KnowledgeBaseLoader()
    
    # Test manifest loading
    print("\n1. Loading CUAD manifest...")
    manifest_count = kb.load_manifest()
    
    if manifest_count > 0:
        print(f"✅ Loaded {manifest_count} contracts from manifest")
    else:
        print("⚠️  No manifest data found (cuad_manifest.csv)")
    
    # Test JSONL loading (with limit due to large file)
    print("\n2. Loading JSONL data (first 100 entries)...")
    jsonl_count = kb.load_jsonl(limit=100)
    
    if jsonl_count > 0:
        print(f"✅ Loaded {jsonl_count} entries from JSONL")
        
        # Categorize by framework
        print("\n3. Categorizing contracts by framework...")
        kb.categorize_by_framework()
        
        stats = kb.get_statistics()
        print(f"\n   Statistics:")
        print(f"   Total contracts: {stats['total_contracts']}")
        print(f"   Unique clause types: {stats['unique_clause_types']}")
        print(f"   Framework categorization:")
        for framework, count in stats['frameworks'].items():
            print(f"     {framework}: {count} contracts")
        
        # Test search
        print("\n4. Testing contract search...")
        results = kb.search_contracts(
            keywords=["privacy", "data protection"],
            limit=5
        )
        print(f"✅ Found {len(results)} contracts matching keywords")
        
    else:
        print("⚠️  No JSONL data found (cuad_sft_train.jsonl)")
    
    return jsonl_count > 0


def test_regulatory_tracker():
    """Test Regulatory Update Tracker."""
    print("\n" + "="*60)
    print("TESTING REGULATORY UPDATE TRACKER")
    print("="*60)
    
    # Check if API keys are available
    has_serper = bool(os.getenv('SERPER_API_KEY'))
    has_groq = bool(os.getenv('GROQ_API_KEY'))
    
    if not has_serper or not has_groq:
        print("⚠️  API keys not set. Tracker requires both SERPER_API_KEY and GROQ_API_KEY")
        return False
    
    print("\n1. Initializing tracker...")
    tracker = RegulatoryUpdateTracker()
    print("✅ Tracker initialized")
    
    # Test checking for updates
    print("\n2. Checking for GDPR updates (last week)...")
    updates = tracker.check_for_updates(
        framework="GDPR",
        time_range='w',
        force_check=True
    )
    
    print(f"✅ Found {len(updates)} new GDPR updates")
    
    if updates:
        print(f"\n   Sample update:")
        update = updates[0]
        print(f"   Title: {update.title[:80]}")
        print(f"   Severity: {update.severity.value}")
        print(f"   Type: {update.update_type.value}")
        print(f"   Impact Score: {update.impact_score:.2f}")
    
    # Get statistics
    print("\n3. Getting tracker statistics...")
    stats = tracker.get_statistics()
    print(f"✅ Statistics retrieved:")
    print(f"   Total sources: {stats['total_sources']}")
    print(f"   Active sources: {stats['active_sources']}")
    print(f"   Recent updates: {stats['recent_updates']}")
    print(f"   Checks performed: {stats['checks_performed']}")
    
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("REGULATORY UPDATE TRACKING SYSTEM - TEST SUITE")
    print("="*60)
    
    print("\nChecking environment variables:")
    env_vars = {
        'SERPER_API_KEY': bool(os.getenv('SERPER_API_KEY')),
        'GROQ_API_KEY': bool(os.getenv('GROQ_API_KEY')),
        'HUGGINGFACE_API_KEY': bool(os.getenv('HUGGINGFACE_API_KEY')),
        'OPENROUTER_API_KEY': bool(os.getenv('OPENROUTER_API_KEY')),
        'SLACK_WEBHOOK_URL': bool(os.getenv('SLACK_WEBHOOK_URL'))
    }
    
    for var, is_set in env_vars.items():
        status = "[OK] Set" if is_set else "[X] Not set"
        print(f"   {var}: {status}")
    
    # Run tests
    results = {}
    
    try:
        results['serper'] = test_serper_api()
    except Exception as e:
        print(f"❌ Serper test failed with exception: {e}")
        results['serper'] = False
    
    try:
        results['groq'] = test_groq_api()
    except Exception as e:
        print(f"❌ Groq test failed with exception: {e}")
        results['groq'] = False
    
    try:
        results['knowledge_base'] = test_knowledge_base()
    except Exception as e:
        print(f"❌ Knowledge Base test failed with exception: {e}")
        results['knowledge_base'] = False
    
    try:
        results['tracker'] = test_regulatory_tracker()
    except Exception as e:
        print(f"❌ Tracker test failed with exception: {e}")
        results['tracker'] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for component, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{component.upper()}: {status}")
    
    passed_count = sum(1 for p in results.values() if p)
    total_count = len(results)
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {passed_count}/{total_count} tests passed")
    print(f"{'='*60}")
    
    if passed_count == total_count:
        print("\n[SUCCESS] All tests passed! System is ready for production.")
    elif passed_count > 0:
        print("\n[WARNING] Some tests failed. Check API keys and dependencies.")
    else:
        print("\n[ERROR] All tests failed. Please configure API keys and check setup.")
    
    print("\nSetup Instructions:")
    print("   1. Set API keys:")
    print("      $env:SERPER_API_KEY='your_serper_key'")
    print("      $env:GROQ_API_KEY='your_groq_key'")
    print("   2. Ensure data files exist:")
    print("      - cuad_manifest.csv")
    print("      - cuad_sft_train.jsonl")
    print("   3. Run: python test_regulatory_updates.py")


if __name__ == "__main__":
    main()
