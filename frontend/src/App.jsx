import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [score, setScore] = useState(null);
  
  // 1. New State to hold our history list!
  const [history, setHistory] = useState([]);

  // 2. Function to fetch history from the Python backend
  const fetchHistory = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/stress/1");
      setHistory(response.data);
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  // 3. This tells React to fetch the history the moment the page loads
  useEffect(() => {
    fetchHistory();
  }, []);

  const handleAnalyze = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/stress/", {
        note: text,
        user_id: 1,
      });
      setScore(response.data.stress_score);
      
      // 4. Automatically refresh the history list after we save a new score!
      fetchHistory();
    } catch (error) {
      alert("Make sure your backend is running!");
      console.error(error);
    }
  };

  return (
    <div className="App">
      <h1>🧠 MindEase AI</h1>
      <p>How are you feeling today?</p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your thoughts here..."
        rows="4"
        cols="50"
      />
      <br />
      <button onClick={handleAnalyze}>Analyze My Stress</button>

      {score !== null && (
        <div className="result">
          <h2>AI Stress Analysis</h2>
          <h3 style={{ color: score > 5 ? "red" : "green" }}>
            Stress Score: {score} / 10
          </h3>
        </div>
      )}

      {/* 5. Our Brand New History Dashboard UI */}
      <div className="history" style={{ marginTop: "40px", textAlign: "left" }}>
        <h3>📖 My Stress History</h3>
        <ul>
          {history.map((entry) => (
            <li key={entry.id} style={{ marginBottom: "10px" }}>
              <strong>Score: {entry.stress_score}/10</strong> - "{entry.note}"
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
