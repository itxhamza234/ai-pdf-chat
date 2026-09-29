import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api";

export default function Chat() {
  const { pdfId } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadHistory() {
    try {
      const data = await api(`/chat/history/${pdfId}`, "GET", null, true);
      setMessages(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadHistory();
  }, [pdfId]);

  async function handleAsk(e) {
    e.preventDefault();
    if (!question.trim()) return;
    setError("");
    setLoading(true);
    try {
      const data = await api("/chat/ask", "POST", { pdf_id: Number(pdfId), question }, true);
      setMessages((prev) => [...prev, { question, answer: data.answer }]);
      setQuestion("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: "50px auto" }}>
      <button onClick={() => navigate("/dashboard")}>← Back to Dashboard</button>
      <h2>Chat</h2>

      <div style={{ border: "1px solid #ccc", padding: 10, height: 400, overflowY: "auto" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 15 }}>
            <p><strong>You:</strong> {m.question}</p>
            <p><strong>AI:</strong> {m.answer}</p>
          </div>
        ))}
        {loading && <p><em>Thinking...</em></p>}
      </div>

      <form onSubmit={handleAsk} style={{ marginTop: 10 }}>
        <input
          style={{ width: "80%" }}
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit" disabled={loading}>Send</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}