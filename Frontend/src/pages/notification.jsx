import React, { useEffect, useState } from 'react';
import '../styles/Notification.css'; // Import the styles
import { useNavigate } from "react-router-dom";
import not from '../assets/not.png';

const Notification = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState({ name: "", email: "" });

  useEffect(() => {
    const queryParams = new URLSearchParams(window.location.search);
    const name = queryParams.get("name");
    const email = queryParams.get("email");

    if (name && email) {
      setUserData({ name, email });
    } else {
      console.error("User data not found");
    }
  }, []);

  const goDashboard = () => {
    navigate("/Dashboard");
  };

  return (
    <div className="notification-prompt-container">
      <div className="content-container">
        <h1>Enable Notifications and <br />Never Miss a Good Deal</h1>
        <p>Turn on notifications and stay up to date with your travel updates.</p>

        {/* Notification Box */}
        <div className="notification-box">
          <div className="notification-content">
            <img src={not} alt="TravelWith" className="notification-logo" />
            <p className="notification-message">Hello {userData.name}, you've received 3 hot deals!</p>
          </div>
        </div>

        {/* Buttons */}
        <div className="buttons-container">
          <button className="enable-btn" onClick={goDashboard}>
            Enable Notifications
          </button>

          <button className="maybe-btn" onClick={goDashboard}>
            Maybe Later
          </button>
        </div>

        <p className="settings-note">You can change settings any time.</p>
      </div>
    </div>
  );
};

export default Notification;
