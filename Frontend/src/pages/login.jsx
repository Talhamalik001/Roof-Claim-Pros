import "../styles/login.css";
import google from "../assets/google.png";
import facebook from "../assets/facebook.png";
import apple from "../assets/apple.png";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from 'axios';

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // ------------------ Google OAuth ------------------
  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:9000/google/login";  // Redirect to Google OAuth
  };
const handleInstagramLogin = () => {
    window.location.href = "http://localhost:9000/instagram/login";  // Redirect to Instagram OAuth
  };
  // ------------------ Facebook OAuth ------------------
const handleFacebookLogin = () => {
  window.location.href = "http://localhost:9000/facebook/login";  // Redirect to Facebook OAuth route
};
  // ------------------ Normal Email Login ------------------
  const handleLogin = async () => {
    if (!email || !password) {
      alert("Please fill both fields");
      return;
    }
// #rahafi5351@him6.com
    try {
      setLoading(true);
      // const res = await axios.post("http://127.0.0.1:9000/auth/login", { email, password });
      const res = await axios.post(
  "http://127.0.0.1:9000/auth/login",
  { email, password },
  { withCredentials: true }
);

      if (res.data.status === "success") {
        alert(`Welcome ${res.data.firstName}!`);
        navigate("/notification");
      }
      // lemur9643513@aminating.com

    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-card">

        <div className="login-icon">↪</div>

        <h2>Sign in with email</h2>
        <p className="subtitle">
          Enter your registered email and password
        </p>

        <div className="input-group">
          <span>📧</span>
          <input 
            type="email" 
            placeholder="Email" 
            value={email} 
            onChange={e => setEmail(e.target.value)} 
          />
        </div>
{/* 12345678QWERqwe!@#$ */}
        <div className="input-group">
          <span>🔒</span>
          <input 
            type="password" 
            placeholder="Password" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
          />
        </div>

        <p className="forgot">Forgot password?</p>

        <button 
          className="primary-btn" 
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? "Signing in..." : "Get Started"}
        </button>

        <p style={{ marginTop: "15px", textAlign: "center" }}>
          Don't have an account?{" "}
          <span 
            style={{ color: "#007bff", cursor: "pointer", fontWeight: "500" }}
            onClick={() => navigate("/create-account")}
          >
            Create Account
          </span>
        </p>

        <div className="divider">
          <span>Or sign in with</span>
        </div>

        <div className="social-buttons">
          <button onClick={handleGoogleLogin}>
            <img src={google} alt="google" />
          </button>
          <button onClick={handleFacebookLogin}>
            <img src={facebook} alt="facebook" />
          </button>
         <button onClick={handleInstagramLogin}>
            <img src={apple} alt="instagram" />
          </button>
        </div>

      </div>
    </div>
  );
}

export default Login;
