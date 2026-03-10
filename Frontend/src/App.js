import React from 'react';
import Login from './pages/login';
import VerifyEmail from './pages/VerifyEmail';
import CreateAccount from './pages/CreateAccount';
import Notification from './pages/notification';
import Dashboard from './pages/Dashboard';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/create-account" element={<CreateAccount />} />
        <Route path="/verify-email" element={<VerifyEmail />} />
        <Route path="/notification" element={<Notification />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
