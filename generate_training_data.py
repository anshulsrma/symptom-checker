# generate_training_data.py
import json

examples = [
    # Small talk / greetings
    ("Hello", "Hi there! How can I help you today?"),
    ("Hi", "Hello! What would you like to know?"),
    ("How are you today?", "I’m doing well, thanks for asking. How are you feeling today?"),

    # Scope guard (non-scope)
    ("Tell me about diabetes.", "I’m not trained on this topic."),
    ("What is hypertension?", "I’m not trained on this topic."),
    ("Can you explain asthma?", "I’m not trained on this topic."),

    # Abdominal pain in adults – general
    ("What are common causes of abdominal pain in adults?",
     "Common causes of abdominal pain in adults include indigestion, gas, stomach viruses, food poisoning, and constipation. Sometimes it can be due to more serious conditions like appendicitis, gallstones, or ulcers."),
    ("What symptoms with abdominal pain are concerning?",
     "Seek urgent care if the pain is severe, persistent, or comes with fever, persistent vomiting, blood in stool or vomit, chest pain, black tarry stools, or if the abdomen is rigid and tender to touch."),
    ("Where can abdominal pain come from?",
     "Abdominal pain can arise from the stomach, intestines, gallbladder, pancreas, liver, urinary tract, or reproductive organs. The location and nature of the pain can help narrow the cause."),
    ("What is right lower abdominal pain in adults?",
     "Right lower abdominal pain in adults can be caused by conditions like appendicitis, ovarian issues, intestinal problems, or muscle strain. Severe or worsening pain should be evaluated by a clinician."),

    # Patterns & related factors
    ("My abdominal pain gets worse after meals—what could it mean?",
     "Pain that worsens after meals may be related to indigestion, gastritis, gallbladder issues, or acid reflux. Keep notes on foods that aggravate your pain and consider medical evaluation."),
    ("I have abdominal pain and fever—what should I do?",
     "Fever with abdominal pain can suggest an infection or inflammation, such as appendicitis or gastroenteritis. If pain is severe or persistent, seek medical care promptly."),
    ("Does stress cause abdominal pain?",
     "Yes, stress and anxiety can contribute to abdominal discomfort, IBS-like symptoms, and changes in bowel habits. Still, new or severe pain should be evaluated by a clinician."),

    # Red flags & when to seek care
    ("When should I see a doctor for abdominal pain?",
     "See a doctor if the pain is severe, persists longer than a day or two, disrupts your activities, or is accompanied by fever, vomiting, blood in stool, chest pain, or fainting."),
    ("Should I go to the emergency room for abdominal pain?",
     "Go to the ER if you have severe, sudden abdominal pain, a rigid abdomen, fever with worsening pain, blood in stool or vomit, chest pain, trouble breathing, or if you feel faint."),

    # Safety (no prescriptions)
    ("What medication should I take for abdominal pain?",
     "I can’t provide prescriptions or specific treatment recommendations. Please consult a qualified healthcare professional for personalized care."),

    # Triaging questions (still within scope)
    ("What questions help figure out abdominal pain cause?",
     "Clinicians often ask about pain location, timing, severity, triggers like meals, bowel changes, fever, vomiting, urinary symptoms, and any recent travel or new medications."),

    # More “not trained”
    ("What is a migraine aura?", "I’m not trained on this topic."),
    ("Knee pain causes?", "I’m not trained on this topic."),
]

with open("training_data.jsonl", "w", encoding="utf-8") as f:
    for user, assistant in examples:
        rec = {"messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant}
        ]}
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print("Wrote training_data.jsonl with", len(examples), "examples.")
