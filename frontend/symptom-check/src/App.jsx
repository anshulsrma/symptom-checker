import React, { useState } from "react";
import "./App.css";

function App() {
  const [step, setStep] = useState(1);
  const [age, setAge] = useState("");
  const [sex, setSex] = useState("");
  const [symptom, setSymptom] = useState("");
  const [details, setDetails] = useState("");
  const [result, setResult] = useState("");

  const [conversation, setConversation] = useState([]);

  const callApi = async (endpoint, body) => {
    const res = await fetch(`http://localhost:5000/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return res.json();
  };

  const handleNextStep = async () => {
    if (step === 1) {
      setStep(step + 1);
      const res = await callApi("start", { age, sex });
      setConversation([...conversation, { role: "assistant", text: res.message }]);
    }
    if (step === 2) {
      setStep(step + 1);
      const res = await callApi("symptom", { symptom });
      setConversation([...conversation, { role: "assistant", text: res.message }]);
    }
    if (step === 3) {
      setStep(step + 1);
      const res = await callApi("details", { details });
      setConversation([...conversation, { role: "assistant", text: res.message }]);
      setResult(res.message);
    }
  };

  const progress = ["GENERAL INFORMATION", "SYMPTOMS", "QUESTIONS", "RESULT"];

  return (
    <div id="root" >
      <div
        style={{
          maxWidth: "600px",
          margin: "auto",
          padding: "30px",
          textAlign: "center",
          fontFamily: "Arial, sans-serif"
        }}
      >
        <h1 style={{ fontSize: "28px", marginBottom: "10px" }}>Symptom Checker</h1>
        <h3 style={{ color: "#00796b", marginBottom: "20px" }}>powered by AI</h3>

        {/* Progress Bar */}
        <div style={{ marginBottom: "20px" }}>
          <p style={{ fontWeight: "bold", color: "#444" }}>
            {progress[step - 1]} (Step {step}/4)
          </p>
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: "10px",
              margin: "10px 0",
            }}
          >
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                style={{
                  height: "6px",
                  width: "60px",
                  borderRadius: "4px",
                  backgroundColor: i <= step ? "#00796b" : "#cfd8dc",
                }}
              />
            ))}
          </div>
        </div>

        {/* Step 1 */}
        {step === 1 && (
          <div>
            <h3>Age</h3>
            <p style={{ color: "#777", marginTop: "-5px" }}>
              Age significantly impacts health risks and wellness strategies.
            </p>
            <input
              type="number"
              placeholder="e.g. 48"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              style={{ padding: "10px", margin: "10px 0", width: "100%" }}
            />

            <h3>Sex assigned at birth</h3>
            <p style={{ color: "#777", marginTop: "-5px" }}>
              Biological sex can impact risk for certain conditions and response to treatments.
            </p>
            <div style={{ display: "flex", justifyContent: "center", gap: "10px" }}>
              <button
                onClick={() => setSex("Male")}
                style={{
                  padding: "10px 20px",
                  backgroundColor: sex === "Male" ? "#b2dfdb" : "#e0f2f1",
                  border: "1px solid #00796b",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                Male
              </button>
              <button
                onClick={() => setSex("Female")}
                style={{
                  padding: "10px 20px",
                  backgroundColor: sex === "Female" ? "#b2dfdb" : "#e0f2f1",
                  border: "1px solid #00796b",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                Female
              </button>
            </div>

            <button
              onClick={handleNextStep}
              disabled={!age || !sex}
              style={{
                marginTop: "20px",
                padding: "10px 20px",
                backgroundColor: "#00796b",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Continue
            </button>
          </div>
        )}

        {/* Step 2 */}
        {step === 2 && (
          <div>
            <h3>Describe your symptoms</h3>
            <p style={{ color: "#777", marginTop: "-5px" }}>
              For accurate insights, provide detailed descriptions of your symptoms.
            </p>
            <textarea
              placeholder="e.g. I have unexpected weight loss and skin changes..."
              value={symptom}
              onChange={(e) => setSymptom(e.target.value)}
              style={{ width: "100%", height: "80px", padding: "10px", marginTop: "10px" }}
            />
            <button
              onClick={handleNextStep}
              disabled={!symptom}
              style={{
                marginTop: "20px",
                padding: "10px 20px",
                backgroundColor: "#00796b",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Continue
            </button>
          </div>
        )}

        {/* Step 3 */}
        {step === 3 && (
          <div>
            <h3>Answer the following questions</h3>
            <p style={{ color: "#777" }}>
              Answer a few questions to refine your symptom analysis.
            </p>
            <ol style={{ textAlign: "left", margin: "20px auto", maxWidth: "500px" }}>
              <li>Can you describe the location and nature of the pain?</li>
              <li>How long have you been experiencing this symptom?</li>
              <li>Have you noticed other symptoms (e.g. fever, nausea)?</li>
            </ol>
            <textarea
              placeholder="Type your answers here..."
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              style={{ width: "100%", height: "100px", padding: "10px", marginTop: "10px" }}
            />
            <button
              onClick={handleNextStep}
              disabled={!details}
              style={{
                marginTop: "20px",
                padding: "10px 20px",
                backgroundColor: "#00796b",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Continue
            </button>
          </div>
        )}

        {/* Step 4 - Final */}
        {step === 4 && result.length == 0 &&(
          <div>
            <h2>🎉 Great Job!</h2>
            <p>You have successfully answered all the questions.</p>
            <p style={{ marginTop: "20px", color: "#00796b" }}>Analyzing health factors...</p>
            <div className="loader" style={{ marginTop: "20px" }}>
              <div
                style={{
                  border: "4px solid #f3f3f3",
                  borderTop: "4px solid #00796b",
                  borderRadius: "50%",
                  width: "30px",
                  height: "30px",
                  animation: "spin 1s linear infinite",
                  margin: "auto",
                }}
              />
            </div>
          </div>
        )}

       {step === 4 && result.length > 0 && (
  <div className="result-container">
    <div className="card">
      <h2 className="title">✅ Symptom Analysis Result</h2>
      <p className="question">
        Based on your responses, here is the summary:
      </p>
      <div className="result-box">
        {result.split("\n").map((line, index) => {
          if (line.startsWith("**") && line.endsWith("**")) {
            // bold headings
            return <h3 key={index}>{line.replace(/\*\*/g, "")}</h3>;
          } else if (line.startsWith("* ")) {
            // bullet points
            return <li key={index}>{line.replace("* ", "")}</li>;
          } else {
            return <p key={index}>{line}</p>;
          }
        })}
      </div>
    </div>
  </div>
)}


      </div>
    </div>
  );
}

export default App;
