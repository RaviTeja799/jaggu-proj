from dotenv import load_dotenv
load_dotenv()

from groq import Groq
import os

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

print("Available Groq Models:")
print("=" * 70)

try:
    models = client.models.list()
    for model in models.data:
        print(f"\n📦 {model.id}")
        if hasattr(model, 'context_window'):
            print(f"   Context: {model.context_window} tokens")
        if hasattr(model, 'description'):
            print(f"   Description: {model.description}")
except Exception as e:
    print(f"Error: {e}")
    print("\nFalling back to known models (as of 2024):")
    known_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "gemma-7b-it"
    ]
    for model in known_models:
        print(f"  • {model}")
