function ResultStep({ userAnswer }) {
  return (
    <div className="result-container">
      <div className="card">
        <h2 className="title">✅ Symptom Analysis Result</h2>
        <p className="question">
          Based on your responses, here is the summary:
        </p>
        <div className="result-box">
          {userAnswer}
        </div>
      </div>
    </div>
  );
}

export default ResultStep;
