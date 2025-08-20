import json
from dataclasses import dataclass
from typing import Dict
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
)
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig

BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"   # change if needed
DATA_PATH = "data/sft_symptoms.jsonl"
OUTPUT_DIR = "out/sft-mistral-symptom-bot"

PROMPT_TEMPLATE = """<s>[INST] You are a cautious medical information assistant.
Respond ONLY using knowledge contained in your training data about symptoms and related factors.
If the user asks for anything outside training, output the special token <NOT_TRAINED> as the entire reply.

User: {instruction}
[/INST]
"""

def formatting_func(example: Dict):
    return PROMPT_TEMPLATE.format(instruction=example["instruction"]) + example["output"]

def main():
    # 4-bit quantization for memory savings (QLoRA)
    bnb = BitsAndBytesConfig(load_in_4bit=True,
                             bnb_4bit_use_double_quant=True,
                             bnb_4bit_compute_dtype="bfloat16",
                             bnb_4bit_quant_type="nf4")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
    # add the special token so model can generate it
    special_tokens = {"additional_special_tokens": ["<NOT_TRAINED>"]}
    tokenizer.add_special_tokens(special_tokens)

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb,
        device_map="auto",
        trust_remote_code=True
    )
    model.resize_token_embeddings(len(tokenizer))

    ds = load_dataset("json", data_files=DATA_PATH)["train"]

    lora = LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05,
        bias="none", task_type="CAUSAL_LM",
        target_modules=["q_proj","k_proj","v_proj","o_proj",
                        "gate_proj","up_proj","down_proj"]  # common for Mistral/Llama
    )

    cfg = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        fp16=False, bf16=True,
        logging_steps=10,
        save_steps=500,
        save_total_limit=2,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        packing=False,
        max_seq_length=1024
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,
        peft_config=lora,
        formatting_func=formatting_func,
        args=cfg
    )

    trainer.train()
    trainer.save_model()
    tokenizer.save_pretrained(OUTPUT_DIR)

if __name__ == "__main__":
    main()
