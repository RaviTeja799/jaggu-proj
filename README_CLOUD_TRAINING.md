# CUAD Legal Clause Extraction - Training Package

## Kaggle Setup (RECOMMENDED)

1. Upload this zip as a Kaggle dataset
2. Create new notebook
3. Enable GPU: Settings → Accelerator → GPU T4 x2
4. Add this dataset to your notebook
5. Run:

```python
import zipfile
import os

# Extract dataset
with zipfile.ZipFile('../input/cuad-training/cuad_kaggle_package.zip', 'r') as z:
    z.extractall('.')

# Install dependencies
!pip install -q peft accelerate bitsandbytes

# Train
!python train_lora.py
```

## Dataset Info

- **Training examples**: 22,450 (408 contracts)
- **Test examples**: 4,182 (102 contracts)
- **Total contracts**: 510
- **Clause categories**: 41
- **Format**: Instruction-tuning (SFT)

## Training Options

### LoRA (Recommended)
```bash
python train_lora.py
```
- Model: Mistral-7B
- Memory: ~12 GB GPU
- Time: 2-3 hours on Kaggle T4 x2

### Output
- **Model**: cuad_lora_model/ (~200-400 MB)
- **Format**: LoRA adapters
- **Usage**: Load with PEFT library

## Troubleshooting

**Out of Memory?**
- Edit train_lora.py: BATCH_SIZE = 1, MAX_LENGTH = 1024

**Model access error?**
- Model already set to Mistral (no auth needed)

**No GPU detected?**
- Settings → Accelerator → GPU T4 x2

## After Training

Download model:
```python
from kaggle_secrets import UserSecretsClient
import shutil

shutil.make_archive('cuad_model', 'zip', 'cuad_lora_model')
# Download from Output tab
```

## License
CUAD Dataset: CC BY 4.0
