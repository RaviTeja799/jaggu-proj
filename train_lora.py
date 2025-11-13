"""
LoRA Fine-tuning Script for CUAD Dataset - Kaggle Optimized
Supports: LLaMA-2, Mistral, Falcon, GPT-2
Requirements: transformers, peft, accelerate, datasets, bitsandbytes
"""
import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from transformers import BitsAndBytesConfig

# ================== CONFIGURATION ==================
MODEL_NAME = "mistralai/Mistral-7B-v0.1"  # No auth needed (change to LLaMA-2 if you have token)
OUTPUT_DIR = "./cuad_lora_model"
MAX_LENGTH = 2048
BATCH_SIZE = 4
GRADIENT_ACCUMULATION = 4
LEARNING_RATE = 2e-4
NUM_EPOCHS = 3
USE_QLORA = True

# LoRA Configuration
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LORA_TARGET_MODULES = ["q_proj", "v_proj", "k_proj", "o_proj"]

print("="*80)
print("CUAD LEGAL CLAUSE EXTRACTION - LORA TRAINING")
print("="*80)
print(f"\nModel: {MODEL_NAME}")
print(f"Output: {OUTPUT_DIR}")
print(f"QLoRA: {USE_QLORA}")
print(f"Epochs: {NUM_EPOCHS}")
print(f"Batch Size: {BATCH_SIZE}")

# ================== LOAD MODEL ==================
print("\nLoading model and tokenizer...")

if USE_QLORA:
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)
else:
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.float16,
    )

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# ================== SETUP LORA ==================
print("\nConfiguring LoRA...")
lora_config = LoraConfig(
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    target_modules=LORA_TARGET_MODULES,
    lora_dropout=LORA_DROPOUT,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ================== LOAD DATASET ==================
print("\nLoading CUAD dataset...")
dataset = load_dataset('json', data_files={
    'train': 'cuad_sft_train.jsonl',
    'test': 'cuad_sft_test.jsonl'
})

print(f"Train examples: {len(dataset['train'])}")
print(f"Test examples: {len(dataset['test'])}")

# ================== PREPROCESSING ==================
def format_instruction(sample):
    prompt = f"""### Instruction:
{sample['instruction']}

### Input:
{sample['input']}

### Response:
{sample['output']}"""
    return prompt

def preprocess_function(examples):
    text = format_instruction(examples)
    tokenized = tokenizer(
        text,
        truncation=True,
        max_length=MAX_LENGTH,
        padding="max_length",
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

print("\nPreprocessing dataset...")
tokenized_dataset = dataset.map(
    preprocess_function,
    batched=False,
    remove_columns=dataset["train"].column_names,
    desc="Tokenizing"
)

# ================== TRAINING ==================
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=NUM_EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION,
    learning_rate=LEARNING_RATE,
    fp16=True,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    logging_steps=10,
    save_total_limit=2,
    load_best_model_at_end=True,
    report_to="none",
    optim="paged_adamw_8bit" if USE_QLORA else "adamw_torch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

print("\n" + "="*80)
print("STARTING TRAINING")
print("="*80)
trainer.train()

# ================== SAVE MODEL ==================
print("\n" + "="*80)
print("SAVING MODEL")
print("="*80)
trainer.save_model()
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"\n✓ Training complete!")
print(f"✓ Model saved to: {OUTPUT_DIR}")
print(f"\nTo use the model:")
print(f"  from peft import AutoPeftModelForCausalLM")
print(f"  model = AutoPeftModelForCausalLM.from_pretrained('{OUTPUT_DIR}')")
print("="*80)
