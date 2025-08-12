import React, { useState, useRef, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Salut! Sunt Smart Librarian. Ce carti it pot recomanda astazi?' }
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    setMessages(prev => [...prev, { sender: 'user', text: question }]);
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ question }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      setMessages(prev => [...prev, { sender: 'bot', text: data.answer }]);
      setQuestion('');
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: 600 }}>
      <h1 className="mb-4">Smart Librarian</h1>
      <div className="border rounded p-3 mb-3 bg-light" style={{ height: 400, overflowY: 'auto' }}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-2 d-flex ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
            <div className={`p-2 rounded ${msg.sender === 'user' ? 'bg-primary text-white' : 'bg-white border'}`}
                 style={{ maxWidth: '80%' }}
                 dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br/>') }} />
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="d-flex gap-2">
        <input
          type="text"
          className="form-control"
          placeholder="Type your question..."
          value={question}
          onChange={e => setQuestion(e.target.value)}
          disabled={loading}
          required
        />
        <button type="submit" className="btn btn-primary" disabled={loading || !question.trim()}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
      {error && (
        <div className="alert alert-danger mt-3">{error}</div>
      )}
    </div>
  );
}

export default App;
