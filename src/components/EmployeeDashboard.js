import React from 'react';
import DashboardLayout from './DashboardLayout';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './Dashboard.css';

const EmployeeDashboard = ({ onNavigate }) => {
  const kpiData = [
    { title: 'Performance Score', value: '4.5/5', change: '+0.2', trend: 'up', icon: '⭐' },
    { title: 'Goals Completed', value: '12/15', change: '80%', trend: 'up', icon: '🎯' },
    { title: 'Learning Hours', value: '24h', change: '+6h', trend: 'up', icon: '📚' },
    { title: 'Tenure', value: '2.5 yrs', change: '', trend: 'up', icon: '⏱️' },
  ];

  const performanceData = [
    { month: 'Jan', score: 4.1 },
    { month: 'Feb', score: 4.2 },
    { month: 'Mar', score: 4.3 },
    { month: 'Apr', score: 4.4 },
    { month: 'May', score: 4.45 },
    { month: 'Jun', score: 4.5 },
  ];

  return (
    <DashboardLayout onNavigate={onNavigate} userRole="employee" currentPage="employee-dashboard">
      <div className="dashboard-header">
        <div>
          <h1>My Dashboard</h1>
          <p className="dashboard-subtitle">Your performance and career development</p>
        </div>
      </div>

      <div className="kpi-grid">
        {kpiData.map((kpi, index) => (
          <div key={index} className="kpi-card">
            <div className="kpi-icon">{kpi.icon}</div>
            <div className="kpi-content">
              <div className="kpi-title">{kpi.title}</div>
              <div className="kpi-value">{kpi.value}</div>
              {kpi.change && (
                <div className={`kpi-change ${kpi.trend}`}>
                  {kpi.trend === 'up' ? '↑' : '↓'} {kpi.change}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="charts-grid">
        <div className="chart-card full-width">
          <h3>My Performance Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="month" stroke="#8b92b0" />
              <YAxis stroke="#8b92b0" domain={[0, 5]} />
              <Tooltip contentStyle={{ background: '#1a1f3a', border: '1px solid #00d4ff' }} />
              <Line type="monotone" dataKey="score" stroke="#00d4ff" strokeWidth={3} dot={{ fill: '#00d4ff', r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default EmployeeDashboard;
