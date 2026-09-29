import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { api } from "../api";

export default function ResetPassword() {
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || "");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await api("/auth/reset-password", "POST", { email, otp, new_password: newPassword });
      setSuccess("Password reset! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "50px auto" }}>
      <h2>Reset Password</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required /><br /><br />
        <input placeholder="OTP Code" value={otp} onChange={(e) => setOtp(e.target.value)} required /><br /><br />
        <input placeholder="New Password" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required /><br /><br />
        <button type="submit">Reset Password</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}
    </div>
  );
}