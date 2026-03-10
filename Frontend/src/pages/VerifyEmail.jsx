import "../styles/verify.css";
import { useState, useRef } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function VerifyEmail() {

  const location = useLocation();
  const navigate = useNavigate();

  const { email, firstName, lastName, password } = location.state;

  const [code, setCode] = useState(["", "", "", "", "", ""]);
  const [loading, setLoading] = useState(false);

  const inputsRef = useRef([]);

  const handleChange = (value, index) => {

    if (!isNaN(value)) {

      const newCode = [...code];
      newCode[index] = value;
      setCode(newCode);

      if (value && index < 5) {
        inputsRef.current[index + 1].focus();
      }

    }

  };

  const handleKeyDown = (e, index) => {

    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1].focus();
    }

  };


  const handleVerify = async () => {

    const otp = code.join("");

    if (otp.length !== 6) {
      alert("Please enter a 6-digit OTP");
      return;
    }

    try {

      setLoading(true);

      const res = await axios.post(
        `${API_BASE_URL}/auth/verify-otp`,
        { email, otp }
      );

      if (res.data.status !== "success") {
        alert("Invalid OTP. Please try again.");
        return;
      }

      await axios.post(
        `${API_BASE_URL}/auth/register`,
        { firstName, lastName, email, password }
      );

      alert("OTP verified and account created successfully!");

      navigate("/notification");

    } catch (err) {

      const message = err.response?.data?.detail;

      if (message === "User already exists") {

        alert("Account already exists. Please login.");
        navigate("/");

      } else {

        alert(message || "Error verifying OTP or registering user.");

      }

      console.error(err);

    } finally {

      setLoading(false);

    }

  };


  const handleResend = async () => {

    try {

      setLoading(true);

      await axios.post(
        `${API_BASE_URL}/auth/send-otp`,
        { email }
      );

      alert("OTP resent to your email!");

    } catch (err) {

      console.error(err);
      alert("Error resending OTP.");

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="verify-wrapper">

      <div className="verify-card">

        <h2>Verify your email</h2>

        <p className="subtitle">
          Enter the 6 digit code we sent to your inbox ({email})
        </p>

        <div className="code-inputs">

          {code.map((digit, index) => (

            <input
              key={index}
              maxLength="1"
              value={digit}
              ref={(el) => (inputsRef.current[index] = el)}
              onChange={(e) => handleChange(e.target.value, index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
            />

          ))}

        </div>

        <p className="resend">

          Didn't get the code?{" "}

          <span
            style={{ cursor: "pointer", color: "blue" }}
            onClick={handleResend}
          >
            Resend it
          </span>

        </p>

        <button
          className="primary-btn"
          onClick={handleVerify}
          disabled={loading}
        >

          {loading ? "Verifying..." : "Continue"}

        </button>

      </div>

    </div>

  );

}

export default VerifyEmail;