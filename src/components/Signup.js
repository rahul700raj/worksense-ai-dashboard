import React, { useState } from 'react';
import './Signup.css';

const Signup = ({ onBack }) => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    company: '',
    password: '',
    confirmPassword: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onBack();
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <div className="signup-header">
          <div className="logo-small">
            <div className="logo-icon-small">WS</div>
            <span>WorkSense AI</span>
          </div>
          <h2>Create Account</h2>
          <p>Start your 14-day free trial</p>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                placeholder="John Doe"
                value={formData.fullName}
                onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Company Name</label>
              <input
                type="text"
                placeholder="Acme Corp"
                value={formData.company}
                onChange={(e) => setFormData({...formData, company: e.target.value})}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label>Work Email</label>
            <input
              type="email"
              placeholder="you@company.com"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              required
            />
          </div>
          <label className="checkbox-label">
            <input type="checkbox" required />
            <span>I agree to the Terms of Service and Privacy Policy</span>
          </label>
          <button type="submit" className="btn-primary">Create Account</button>
        </form>
        <div className="signin-link">
          Already have an account? <a href="#" onClick={onBack}>Sign in</a>
        </div>
      </div>
    </div>
  );
};

export default Signup;
