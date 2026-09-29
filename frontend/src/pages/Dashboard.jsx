import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api, uploadFile } from "../api";

export default function Dashboard() {
  const [pdfs, setPdfs] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function loadPdfs() {
    try {
      const data = await api("/pdf/list", "GET", null, true);
      setPdfs(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadPdfs();
  }, []);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return;
    setError("");
    setUploading(true);
    try {
      await uploadFile("/pdf/upload", file);
      setFile(null);
      await loadPdfs();
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(id) {
    try {
      await api(`/pdf/${id}`, "DELETE", null, true);
      await loadPdfs();
    } catch (err) {
      setError(err.message);
    }
  }

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/login");
  }

  return (
    <div style={{ maxWidth: 600, margin: "50px auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>Your PDFs</h2>
        <div>
          <Link to="/profile" style={{ marginRight: 10 }}>Profile</Link>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <form onSubmit={handleUpload}>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" disabled={uploading}>
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {pdfs.map((pdf) => (
          <li key={pdf.id} style={{ margin: "10px 0" }}>
            {pdf.filename}
            <button style={{ marginLeft: 10 }} onClick={() => navigate(`/chat/${pdf.id}`)}>Chat</button>
            <button style={{ marginLeft: 10 }} onClick={() => handleDelete(pdf.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}