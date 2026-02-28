import React from 'react';
import DashboardLayout from './DashboardLayout';
import './Dashboard.css';

const AttritionRisk = ({ onNavigate, userRole }) => {
  const highRiskEmployees = [
    { name: 'Sarah Johnson', role: 'Senior Engineer', score: 87, level: 'high' },
    { name: 'Michael Chen', role: 'Product Manager', score: 82, level: 'high' },
    { name: 'Emily Davis', role: 'UX Designer', score: 78, level: 'high' },
    { name: 'James Wilson', role: 'Data Scientist', score: 65, level: 'medium' },
    { name: 'Lisa Anderson', role: 'Marketing Lead', score: 58, level: 'medium' },
  ];

  const getRiskClass = (level) => {
    if (level === 'high') return 'high';
    if (level === 'medium') return 'medium';
    return 'low';
  };

  return (
    <DashboardLayout onNavigate={onNavigate} userRole={userRole} currentPage="attrition-risk">
      <div className="dashboard-header">
        <div>
          <h1>Attrition Risk Analysis</h1>
          <p className="dashboard-subtitle">AI-predicted employee retention risks</p>
        </div>
      </div>

      <div className="insight-card">
        <div className="insight-header">
          <span className="insight-icon">⚠️</span>
          <h3 className="insight-title">Risk Overview</h3>
        </div>
        <p className="insight-content">
          Our AI model has identified 5 employees at elevated risk of attrition based on engagement scores, 
          performance trends, tenure, and market conditions.
        </p>
        <div className="insight-metrics">
          <div className="metric-item">
            <div className="metric-label">High Risk</div>
            <div className="metric-value">3</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Medium Risk</div>
            <div className="metric-value">2</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Potential Cost</div>
            <div className="metric-value">$450K</div>
          </div>
        </div>
      </div>

      <div className="chart-card">
        <h3>High-Risk Employees</h3>
        <div className="risk-list">
          {highRiskEmployees.map((employee, index) => (
            <div key={index} className="risk-item">
              <div className="risk-info">
                <div className="risk-avatar">
                  {employee.name.split(' ').map(n => n[0]).join('')}
                </div>
                <div className="risk-details">
                  <h4>{employee.name}</h4>
                  <p>{employee.role}</p>
                </div>
              </div>
              <div className="risk-score">
                <div className="risk-label">Risk Score</div>
                <div className={`risk-value ${getRiskClass(employee.level)}`}>
                  {employee.score}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default AttritionRisk;
