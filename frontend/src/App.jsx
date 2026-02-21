import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [note, setNote] = useState('')
  const [aiScore, setAiScore] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setLoading(true)
    setAiScore(null)

    try {
      // Sending the text to your FastAPI backend!
      const response = await axios.post('http://127.0.0.1:8000/stress', {
        user_id: 1, // Using the dummy user we created earlier
        stress_score: 0,
        note: note
      })
      
      // Setting the score returned by your Joblib ML model
      setAiScore(response.data.data.stress_score || response.data.stress_score)
    } catch (error) {
      console.error("Error connecting to AI:", error)
      alert("Make sure your backend is running!")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container" style={{ maxWidth: '600px', margin: '50px auto', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1>🧠 MindEase AI</h1>
      <p>How are you feeling today?</p>
      
      <form onSubmit={handleAnalyze}>
        <textarea 
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Type your thoughts here... (e.g., 'I am so stressed about my upcoming exams')"
          rows="5"
          style={{ width: '100%', padding: '10px', fontSize: '16px', borderRadius: '8px', marginBottom: '15px' }}
          required
        />
        <br />
        <button 
          type="submit" 
          disabled={loading}
          style={{ padding: '10px 20px', fontSize: '18px', cursor: 'pointer', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '5px' }}
        >
          {loading ? 'Analyzing...' : 'Analyze My Stress'}
        </button>
      </form>

      {aiScore !== null && (
        <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f4f4f9', borderRadius: '8px' }}>
          <h2>AI Stress Analysis</h2>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: aiScore >= 7 ? 'red' : aiScore >= 4 ? 'orange' : 'green' }}>
            Stress Score: {aiScore} / 10
          </p>
        </div>
      )}
    </div>
  )
}

export default App
