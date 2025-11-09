from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

print("Loading environment variables from .env...")
print()

from services.groq_service import GroqService
from services.serper_service import SerperService

print("Testing APIs with loaded environment variables...")
print()

# Test Serper
print("1. Testing Serper API...")
serper = SerperService()
if serper.test_connection():
    print("   ✓ Serper API: Connected successfully!")
    
    # Try a quick search
    try:
        results = serper.search("GDPR compliance", num_results=3)
        print(f"   ✓ Search test: Found {len(results.get('organic', []))} results")
    except Exception as e:
        print(f"   ⚠ Search test failed: {e}")
else:
    print("   ✗ Serper API: Connection failed")

print()

# Test Groq
print("2. Testing Groq API...")
groq = GroqService()
if groq.test_connection():
    print("   ✓ Groq API: Connected successfully!")
    
    # Try generating a clause
    try:
        print("   Testing clause generation...")
        clause_result = groq.generate_compliant_clause(
            clause_type="Data Processing",
            framework="GDPR",
            context="Cloud storage provider",
            model="llama-3.1-70b-versatile"
        )
        print("   ✓ Clause generation successful!")
        print()
        print("   Generated clause preview:")
        print("   " + "-" * 66)
        clause_text = clause_result.get('clause', 'No clause')
        # Print first 200 chars
        print("   " + clause_text[:200].replace('\n', '\n   '))
        if len(clause_text) > 200:
            print("   ...")
        print()
    except Exception as e:
        print(f"   ✗ Clause generation failed: {e}")
else:
    print("   ✗ Groq API: Connection failed")

print()
print("="*70)
print("API INTEGRATION TEST COMPLETE")
print("="*70)
