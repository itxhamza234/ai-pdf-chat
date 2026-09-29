import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage("");
    try {
      await api("/auth/forgot-password", "POST", { email });
      setMessage("If this email is registered, an OTP has been sent.");
      setTimeout(() => navigate("/reset-password", { state: { email } }), 1500);
    } catch (err) {
      setMessage(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "50px auto" }}>
      <h2>Forgot Password</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /><br /><br />
        <button type="submit">Send OTP</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}