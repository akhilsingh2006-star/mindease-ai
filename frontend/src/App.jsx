import { useState, useEffect } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [score, setScore] = useState(null);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchHistory = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/stress/1");
      setHistory(response.data);
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/stress/", {
        note: text,
        user_id: 1,
      });
      setScore(response.data.stress_score);
      fetchHistory();
      setText(""); 
    } catch (error) {
      alert("Make sure your backend is running!");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  // Recharts looks best when data goes from oldest (left) to newest (right).
  // Our Python API sends the newest first, so we reverse a copy of the array here!
  const chartData = [...history].reverse();

  return (
    <div className="App">
      <h1>🧠 MindEase AI</h1>
      <p>How are you feeling today?</p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your thoughts here..."
        rows="4"
      />
      
      <button onClick={handleAnalyze} disabled={isLoading}>
        {isLoading ? "🧠 AI is thinking..." : "Analyze My Stress"}
      </button>

      {score !== null && (
        <div className="result">
          <h2>AI Stress Analysis</h2>
          <h3 style={{ color: score > 5 ? "#e53e3e" : "#38a169" }}>
            Stress Score: {score} / 10
          </h3>
        </div>
      )}

      {/* --- The New Interactive Chart --- */}
      {history.length > 0 && (
        <div style={{ marginTop: "40px", height: "300px", background: "rgba(255,255,255,0.9)", padding: "20px", borderRadius: "16px", boxShadow: "0 4px 6px rgba(0,0,0,0.05)" }}>
          <h3 style={{ color: "#2d3748", marginBottom: "20px", textAlign: "left" }}>📈 My Stress Trend</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="id" tick={{ fill: '#718096' }} />
              <YAxis domain={[0, 10]} tick={{ fill: '#718096' }} />
              <Tooltip 
                contentStyle={{ borderRadius: '10px', border: 'none', boxShadow: '0 4px 15px rgba(0,0,0,0.1)' }}
              />
              <Line 
                type="monotone" 
                dataKey="stress_score" 
                stroke="#667eea" 
                strokeWidth={4} 
                activeDot={{ r: 8 }} 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="history">
        <h3>📖 Stress Log</h3>
        <ul>
          {history.map((entry) => (
            <li key={entry.id}>
              <strong>Score: {entry.stress_score}/10</strong> - "{entry.note}"
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;