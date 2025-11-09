"""Find HuggingFace library locations"""
from pathlib import Path
import sys

print("=" * 60)
print("HUGGINGFACE LIBRARIES LOCATION")
print("=" * 60)

# Virtual environment location
venv_path = Path("E:/323103310024/Updated Infosys/jaggu-proj/.venv")
site_packages = venv_path / "Lib" / "site-packages"

print(f"\n📦 Virtual Environment:")
print(f"   {venv_path}")

print(f"\n📚 Site Packages Directory:")
print(f"   {site_packages}")

print("\n" + "=" * 60)
print("INSTALLED HUGGINGFACE PACKAGES")
print("=" * 60)

# Find HuggingFace related packages
if site_packages.exists():
    hf_packages = []
    for item in site_packages.iterdir():
        name = item.name.lower()
        if any(keyword in name for keyword in ['hugging', 'transformers', 'tokenizers', 'sentence']):
            hf_packages.append(item)
    
    print()
    for pkg in sorted(hf_packages):
        if pkg.is_dir():
            # Calculate size
            try:
                size = sum(f.stat().st_size for f in pkg.rglob('*') if f.is_file())
                size_mb = size / (1024 * 1024)
                print(f"📁 {pkg.name}")
                print(f"   Location: {pkg}")
                print(f"   Size: {size_mb:.1f} MB")
                print()
            except:
                print(f"📁 {pkg.name}")
                print(f"   Location: {pkg}")
                print()

# Model cache location
print("=" * 60)
print("MODEL CACHE LOCATION")
print("=" * 60)

cache_dir = Path.home() / '.cache' / 'huggingface'
print(f"\n💾 Models Cache Directory:")
print(f"   {cache_dir}")
print(f"   Exists: {cache_dir.exists()}")

if cache_dir.exists():
    hub_dir = cache_dir / 'hub'
    if hub_dir.exists():
        print(f"\n📦 Downloaded Models: {hub_dir}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
The HuggingFace libraries are installed in two locations:

1. LIBRARY CODE (Python packages):
   E:/323103310024/Updated Infosys/jaggu-proj/.venv/Lib/site-packages/
   - transformers/
   - huggingface_hub/
   - tokenizers/
   - sentence_transformers/

2. MODEL FILES (Downloaded AI models):
   C:/Users/raviteja/.cache/huggingface/hub/
   - models--nlpaueb--legal-bert-base-uncased/
   - models--sentence-transformers--all-MiniLM-L6-v2/
   - ... other models
""")
