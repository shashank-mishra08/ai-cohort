import { useState } from 'react'
import './App.css'

/**
 * Day 3 scaffold — React frontend shell.
 * Later days will connect this UI to the FastAPI /chat endpoint.
 */
function App() {
  const [message, setMessage] = useState('')
  const [log, setLog] = useState([
    {
      role: 'assistant',
      text: 'Coverage chatbot UI scaffold (Day 3). Backend + chat wiring come in later days.',
    },
  ])

  function send(e) {
    e.preventDefault()
    const text = message.trim()
    if (!text) return
    setLog((prev) => [
      ...prev,
      { role: 'user', text },
      {
        role: 'assistant',
        text: '(Placeholder) Connect this form to FastAPI /chat in a later day.',
      },
    ])
    setMessage('')
  }

  return (
    <main style={{ maxWidth: 640, margin: '2rem auto', fontFamily: 'system-ui' }}>
      <h1>Coverage Chatbot</h1>
      <p style={{ color: '#555' }}>
        React + Vite scaffold for the healthcare coverage chatbot program.
      </p>

      <div
        style={{
          border: '1px solid #ddd',
          borderRadius: 8,
          padding: 12,
          minHeight: 240,
          marginBottom: 12,
          background: '#fafafa',
        }}
      >
        {log.map((m, i) => (
          <p key={i} style={{ margin: '0.5rem 0' }}>
            <strong>{m.role === 'user' ? 'You' : 'Bot'}:</strong> {m.text}
          </p>
        ))}
      </div>

      <form onSubmit={send} style={{ display: 'flex', gap: 8 }}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask about coverage (UI only for now)…"
          style={{ flex: 1, padding: 8 }}
        />
        <button type="submit">Send</button>
      </form>
    </main>
  )
}

export default App
