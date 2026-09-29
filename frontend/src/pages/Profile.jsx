import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function loadProfile() {
    try {
      const data = await api("/user/me", "GET", null, true);
      setProfile(data);
      setName(data.name);
      setEmail(data.email);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadProfile();
  }, []);

  async function handleUpdate(e) {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      await api("/user/me", "PUT", { name, email }, true);
      setMessage("Profile updated successfully.");
      loadProfile();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleChangePassword(e) {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      await api("/user/change-password", "POST", {
        current_password: currentPassword,
        new_password: newPassword,
      }, true);
      setMessage("Password changed successfully.");
      setCurrentPassword("");
      setNewPassword("");
    } catch (err) {
      setError(err.message);
    }
  }

  if (!profile) return <p>Loading...</p>;

  return (
    <div style={{ maxWidth: 400, margin: "50px auto" }}>
      <Link to="/dashboard">← Back to Dashboard</Link>
      <h2>My Profile</h2>
      <p>Verified: {profile.is_verified ? "Yes" : "No"}</p>

      <h3>Update Profile</h3>
      <form onSubmit={handleUpdate}>
        <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} /><br /><br />
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} /><br /><br />
        <button type="submit">Update</button>
      </form>

      <h3>Change Password</h3>
      <form onSubmit={handleChangePassword}>
        <input placeholder="Current Password" type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} required /><br /><br />
        <input placeholder="New Password" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required /><br /><br />
        <button type="submit">Change Password</button>
      </form>

      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}