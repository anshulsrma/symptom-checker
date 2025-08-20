from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import subprocess

app = Flask(__name__)
CORS(app)  # allow React frontend to call Flask backend

conversation_state = {
    "age": None,
    "sex": None,
    "symptom": None,
    "details": None
}

# ------------------------------
# Query Ollama helper
# ------------------------------
def query_ollama(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],  # replace with your model
            input=prompt,
            text=True,
            encoding="utf-8",      # ✅ force utf-8
            errors="ignore",       # ✅ skip bad chars instead of crashing
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error communicating with Ollama: {e.stderr}"

@app.route("/start", methods=["POST"])
def start():
    data = request.json
    conversation_state["age"] = data.get("age")
    conversation_state["sex"] = data.get("sex")
    return jsonify({"message": "Thanks! Now, what symptom are you experiencing?"})

@app.route("/symptom", methods=["POST"])
def symptom():
    data = request.json
    conversation_state["symptom"] = data.get("symptom")

    if conversation_state["symptom"].lower() == "abdominal pain":
        return jsonify({
            "message": """Answer the following questions to refine your symptom analysis:
- Can you describe the location and intensity of the abdominal pain? Is it sharp, dull, cramping, or burning?
- Have you noticed any other symptoms such as nausea, vomiting, diarrhea, constipation, or changes in appetite?
- Have you experienced any recent changes in your diet, stress levels, or had any recent injuries or illnesses?"""
        })
    else:
        return jsonify({"message": "Currently, I’m trained only for 'Abdominal pain in adults'."})

@app.route("/details", methods=["POST"])
def details():
    data = request.json
    conversation_state["details"] = data.get("details")

    user_input = f"""
Patient info:
- Age: {conversation_state['age']}
- Sex: {conversation_state['sex']}
- Symptom: {conversation_state['symptom']}
- Details: {conversation_state['details']}
"""
    print(user_input)
# Build structured prompt for Ollama
    prompt = f"""
You are a cautious medical assistant trained ONLY on "Abdominal pain in adults".

{user_input}

Task:
- Provide possible differential diagnoses related to abdominal pain.
- Rank them with High / Moderate / Low probability.
- Keep explanation clear and human-like.
- Do NOT suggest prescriptions or treatments.
- Encourage consulting a doctor.
"""

    # Query Ollama or fallback to canned response
    # response = ollama.chat(
    #     model="llama3.1:8b", 
    #     messages=[{"role": "system", "content": "You are a medical assistant trained only on 'Abdominal pain in adults'."},
    #               {"role": "user", "content": user_input}]
    # )
    
    response = query_ollama(prompt)
    print("Ollama response:", response)
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
