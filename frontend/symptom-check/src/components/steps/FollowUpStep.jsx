import { useState } from "react";

function FollowUpStep({ onNext }) {
  const [answer, setAnswer] = useState("");

  const handleNext = () => {
    if (answer.trim() !== "") {
      // Pass answer to parent (can be stored or sent to API)
      onNext(answer);
      setAnswer("");
    }
  };

  return (
    <div className="followup-container">
      <div className="card">
        <h2 className="title">🤖 Follow-up Question</h2>
        <p className="question">
          Answer the following questions to refine your symptom analysis:
          <br />• Can you describe the location and intensity of the abdominal pain?
          <br />• Have you noticed any other symptoms such as nausea, vomiting, diarrhea, constipation, or changes in appetite?
          <br />• Have you experienced any recent changes in diet, stress levels, or had any recent injuries/illnesses?
        </p>

        {/* Input */}
        <textarea
          className="input-box"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your response here..."
        />

        {/* Next Button */}
        <button className="next-btn" onClick={handleNext}>
          Next ➡
        </button>
      </div>
    </div>
  );
}

export default FollowUpStep;
