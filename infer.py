import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
from peft import PeftModel
import json

GEN_MODEL_DIR = "out/sft-mistral-symptom-bot"
GATE_MODEL_DIR = "out/gate-minilm"
REFUSAL_TOKEN = "<NOT_TRAINED>"
REFUSAL_TEXT = "I'm not trained on this topic."

# --- Load generator (LoRA on base) ---
gen_tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL_DIR, use_fast=True)
gen_model = AutoModelForCausalLM.from_pretrained(
    GEN_MODEL_DIR,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

# --- Load gate classifier ---
gate_tokenizer = AutoTokenizer.from_pretrained(GATE_MODEL_DIR, use_fast=True)
gate_model = AutoModelForSequenceClassification.from_pretrained(
    GATE_MODEL_DIR,
    torch_dtype=torch.float16,
    device_map="auto"
)

def is_in_domain(text: str, threshold: float = 0.5) -> bool:
    inputs = gate_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256).to(gate_model.device)
    with torch.no_grad():
        logits = gate_model(**inputs).logits
        probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]
    return probs[1] >= threshold  # label 1 == in-domain

PROMPT = """<s>[INST] You are a cautious medical information assistant.
Respond ONLY using knowledge contained in your training data about symptoms and related factors.
If the user asks for anything outside training, output the special token <NOT_TRAINED> as the entire reply.

User: {question}
[/INST]
"""

def answer(question: str) -> str:
    # Step 1: gate
    if not is_in_domain(question):
        return REFUSAL_TEXT

    # Step 2: generate
    prompt = PROMPT.format(question=question)
    inputs = gen_tokenizer(prompt, return_tensors="pt").to(gen_model.device)
    with torch.no_grad():
        out = gen_model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,   # deterministic helps avoid drift
            temperature=0.0,
            eos_token_id=gen_tokenizer.eos_token_id
        )
    text = gen_tokenizer.decode(out[0], skip_special_tokens=True)
    # Extract only the assistant part (simple split; adjust if your template differs)
    reply = text.split("User:")[-1]  # crude; you can refine parsing
    # Final guard: if model says not trained
    if REFUSAL_TOKEN in text:
        return REFUSAL_TEXT
    return text.split("[/INST]")[-1].strip()

if __name__ == "__main__":
    print("Symptom bot ready. Type 'quit' to exit.")
    while True:
        q = input("Patient: ")
        if q.strip().lower() == "quit":
            break
        print("Assistant:", answer(q))
