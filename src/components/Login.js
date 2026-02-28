import React, { useState } from 'react';
import './Login.css';

const Login = ({ onLogin, onSignup }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('hr');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(role);
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="login-branding">
          <div className="logo-container">
            <div className="logo-icon">WS</div>
            <h1 className="logo-text">WorkSense AI</h1>
          </div>
          <p className="tagline">Intelligent HR Analytics for Modern Enterprises</p>
          <div className="features">
            <div className="feature-item">
              <span className="feature-icon">🤖</span>
              <span>AI-Powered Insights</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">📊</span>
              <span>Real-time Analytics</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🎯</span>
              <span>Predictive Modeling</span>
            </div>
          </div>
        </div>
      </div>
      <div className="login-right">
        <div className="login-box">
          <h2>Welcome Back</h2>
          <p className="login-subtitle">Sign in to your account</p>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Login As</label>
              <select value={role} onChange={(e) => setRole(e.target.value)}>
                <option value="hr">HR Admin</option>
                <option value="manager">Manager</option>
                <option value="employee">Employee</option>
              </select>
            </div>
            <div className="form-options">
              <label className="checkbox-label">
                <input type="checkbox" />
                <span>Remember me</span>
              </label>
              <a href="#" className="forgot-link">Forgot password?</a>
            </div>
            <button type="submit" className="btn-primary">Sign In</button>
          </form>
          <div className="signup-link">
            Don't have an account? <a href="#" onClick={onSignup}>Sign up</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
