"""Verify Kaggle package"""
import os
from pathlib import Path

print("="*70)
print("KAGGLE PACKAGE VERIFICATION")
print("="*70)

required = ["cuad_sft_train.jsonl", "cuad_sft_test.jsonl", "train_lora.py"]
print("\nChecking required files:")
for f in required:
    exists = Path(f).exists()
    print(f"  {'✓' if exists else '✗'} {f}")

print("\nChecking GPU:")
try:
    import torch
    if torch.cuda.is_available():
        print(f"  ✓ GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("  ✗ No GPU! Enable GPU in Kaggle settings")
except:
    print("  ⚠ PyTorch not installed")

print("="*70)
