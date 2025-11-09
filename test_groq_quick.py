from services.groq_service import GroqService

print("Testing Groq connection with updated model...")
groq = GroqService()
result = groq.test_connection()

if result:
    print("✓ Groq API: Connected successfully!")
    print("\nTrying to generate a sample clause...")
    
    try:
        clause_result = groq.generate_compliant_clause(
            clause_type="Data Processing",
            framework="GDPR",
            context="Cloud storage provider",
            model="llama-3.1-70b-versatile"
        )
        print("✓ Clause generation successful!")
        print(f"\nGenerated clause preview:")
        print("-" * 70)
        print(clause_result.get('clause', 'No clause')[:300] + "...")
    except Exception as e:
        print(f"✗ Clause generation failed: {e}")
else:
    print("✗ Groq API: Connection failed")
