import json
from datasets import load_dataset, ClassLabel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import evaluate
import numpy as np

BASE = "sentence-transformers/all-MiniLM-L6-v2"   # small & fast
DATA_PATH = "data/gate_train.jsonl"
OUTPUT_DIR = "out/gate-minilm"

def preprocess(examples, tokenizer):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=256)

def main():
    ds = load_dataset("json", data_files=DATA_PATH)["train"]
    ds = ds.class_encode_column("label")

    tokenizer = AutoTokenizer.from_pretrained(BASE)
    model = AutoModelForSequenceClassification.from_pretrained(BASE, num_labels=2)

    encoded = ds.map(lambda x: preprocess(x, tokenizer), batched=True)
    encoded = encoded.train_test_split(test_size=0.1, seed=42)

    acc = evaluate.load("accuracy")
    f1 = evaluate.load("f1")

    def compute_metrics(p):
        preds = np.argmax(p.predictions, axis=1)
        return {
            "accuracy": acc.compute(predictions=preds, references=p.label_ids)["accuracy"],
            "f1": f1.compute(predictions=preds, references=p.label_ids, average="macro")["f1"]
        }

    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        num_train_epochs=3,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1"
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=encoded["train"],
        eval_dataset=encoded["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    trainer.train()
    trainer.save_model()
    tokenizer.save_pretrained(OUTPUT_DIR)

if __name__ == "__main__":
    main()
