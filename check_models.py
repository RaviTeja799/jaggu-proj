"""Check if AI models are downloaded"""
from pathlib import Path
import os

# Check HuggingFace cache
cache_dir = Path.home() / '.cache' / 'huggingface'
print(f"HuggingFace cache directory: {cache_dir}")
print(f"Cache exists: {cache_dir.exists()}")

if cache_dir.exists():
    hub_dir = cache_dir / 'hub'
    if hub_dir.exists():
        models = [d for d in os.listdir(hub_dir) if d.startswith('models--')]
        print(f"\n✓ Found {len(models)} downloaded models:\n")
        
        for model_dir in sorted(models):
            model_name = model_dir.replace('models--', '').replace('--', '/')
            model_path = hub_dir / model_dir
            
            # Get size
            total_size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            
            print(f"  📦 {model_name}")
            print(f"     Size: {size_mb:.1f} MB")
            print()
    else:
        print("\n⚠ No models downloaded yet - hub directory doesn't exist")
else:
    print("\n⚠ No models downloaded yet - cache directory doesn't exist")

print("\nRequired models for this project:")
print("  1. nlpaueb/legal-bert-base-uncased (LegalBERT) - ~440 MB")
print("  2. sentence-transformers/all-MiniLM-L6-v2 - ~90 MB")
print("  3. meta-llama/Llama-2-13b-chat-hf (Optional) - ~13 GB")
print("\nModels will be automatically downloaded on first use.")
