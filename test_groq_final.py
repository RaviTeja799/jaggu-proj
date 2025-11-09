from dotenv import load_dotenv
load_dotenv()

from services.groq_service import GroqService

print("="*70)
print("GROQ API TEST - CLAUSE GENERATION")
print("="*70)
print()

groq = GroqService()

print("✓ Groq service initialized")
print()

print("Generating compliant Data Processing clause for GDPR...")
print("-"*70)

try:
    result = groq.generate_compliant_clause(
        clause_type="Data Processing",
        framework="GDPR",
        context="Cloud storage provider handling customer data in the EU",
        issues=["Missing data retention policy", "No data subject rights mention"],
        model="llama-3.3-70b-versatile"
    )
    
    print("\n✓ SUCCESS! Generated compliant clause:")
    print("="*70)
    print(result.get('clause', 'No clause generated'))
    print("="*70)
    
    if 'explanation' in result:
        print("\n📝 Explanation:")
        print("-"*70)
        print(result['explanation'])
    
    if 'key_points' in result and result['key_points']:
        print("\n🔑 Key Compliance Points:")
        for i, point in enumerate(result['key_points'], 1):
            print(f"  {i}. {point}")
    
    print("\n" + "="*70)
    print("✅ GROQ API WORKING PERFECTLY!")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPlease check:")
    print("  1. GROQ_API_KEY is set in .env")
    print("  2. API key is valid")
    print("  3. Model name is correct")
