import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Signup from "./pages/Signup";
import VerifyOtp from "./pages/VerifyOtp";
import Login from "./pages/Login";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";

function isLoggedIn() {
  return !!localStorage.getItem("token");
}

function Protected({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/verify-otp" element={<VerifyOtp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
        <Route path="/chat/:pdfId" element={<Protected><Chat /></Protected>} />
        <Route path="*" element={<Navigate to={isLoggedIn() ? "/dashboard" : "/login"} />} />
        <Route path="/profile" element={<Protected><Profile /></Protected>} />
      </Routes>
    </BrowserRouter>
  );
}