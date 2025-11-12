"""
Test script to debug CUAD-to-regulatory mapping
"""
import sys
from services.legal_bert_classifier import LegalBERTClassifier

print("=" * 80)
print("CUAD-TO-REGULATORY MAPPING DEBUG TEST")
print("=" * 80)

# Initialize classifier
print("\n1. Initializing LegalBERTClassifier...")
classifier = LegalBERTClassifier()

# Check if mapping exists
print("\n2. Checking cuad_to_regulatory_mapping dictionary...")
print(f"   Mapping exists: {hasattr(classifier, 'cuad_to_regulatory_mapping')}")
print(f"   Mapping entries: {len(classifier.cuad_to_regulatory_mapping) if hasattr(classifier, 'cuad_to_regulatory_mapping') else 0}")

# Test some common CUAD types
test_types = [
    "Non-Compete",
    "Audit Rights",
    "Data Processing",  # Original type
    "Confidentiality",
    "IP Ownership",
    "Governing Law",
    "Unknown Type"
]

print("\n3. Testing mapping for common clause types:")
print("-" * 80)
for cuad_type in test_types:
    regulatory_type = classifier.get_regulatory_clause_type(cuad_type)
    print(f"   '{cuad_type}' → '{regulatory_type}'")

print("\n4. Checking all mapping entries:")
print("-" * 80)
if hasattr(classifier, 'cuad_to_regulatory_mapping'):
    for cuad_type, reg_type in sorted(classifier.cuad_to_regulatory_mapping.items())[:10]:
        print(f"   '{cuad_type}' → '{reg_type}'")
    if len(classifier.cuad_to_regulatory_mapping) > 10:
        print(f"   ... and {len(classifier.cuad_to_regulatory_mapping) - 10} more mappings")
else:
    print("   ❌ Mapping dictionary not found!")

print("\n" + "=" * 80)
print("Test completed!")
print("=" * 80)
