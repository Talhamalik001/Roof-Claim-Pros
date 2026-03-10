import React, { useState } from 'react';
import '../styles/CreateAccount.css';
import google from '../assets/google.png';
import facebook from '../assets/facebook.png';
import apple from '../assets/apple.png';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

const CreateAccount = () => {
  const navigate = useNavigate();

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!firstName || !lastName || !email || !password) {
      alert('Please fill all the fields');
      return;
    }

    if (password.length < 8 || !/\d/.test(password) || !/[a-zA-Z]/.test(password)) {
      alert('Password must be at least 8 characters and contain a letter and a number');
      return;
    }

    if (!termsAccepted) {
      alert('You must accept the terms and conditions');
      return;
    }

    try {
      setLoading(true);

      await axios.post('http://127.0.0.1:9000/auth/send-otp', { email });

      alert('OTP sent to your email!');

      navigate('/verify-email', { state: { email, firstName, lastName, password } });

    } catch (err) {
      console.error(err);
      alert('Error sending OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-account-container">
      <div className="form-container">
        <h1>Place where all your Travels begin</h1>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="First name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />

          <input
            type="text"
            placeholder="Last name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength="8"
          />

          <p>At least 8 characters, containing a letter and a number</p>

          <div className="terms">
            <input
              type="checkbox"
              id="termss"
              checked={termsAccepted}
              onChange={() => setTermsAccepted(!termsAccepted)}
            />

            <label htmlFor="termss">
              Creating an account, you agree to our
              <a href="#"> Terms of Service </a>
              and
              <a href="#"> Privacy Policy</a>.
            </label>
          </div>

          <button
            type="submit"
            className="primary-btn"
            disabled={loading}
          >
            {loading ? 'Sending OTP...' : 'Create Account'}
          </button>
        </form>

        {/* 👇 Sign In Link */}
        <p style={{ marginTop: "15px", textAlign: "center" }}>
          Already have an account?{" "}
          <span
            style={{ color: "#007bff", cursor: "pointer", fontWeight: "500" }}
            onClick={() => navigate("/")}
          >
            Sign In
          </span>
        </p>

        <div className="social-buttons">
          <button className="social-btn google-btn">
            <img src={google} alt="google" />
          </button>

          <button className="social-btn facebook-btn">
            <img src={facebook} alt="facebook" />
          </button>

          <button className="social-btn apple-btn">
            <img src={apple} alt="apple" />
          </button>
        </div>

      </div>
    </div>
  );
};

export default CreateAccount;