import React from 'react';
import DashboardLayout from './DashboardLayout';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './Dashboard.css';

const ManagerDashboard = ({ onNavigate }) => {
  const kpiData = [
    { title: 'Team Size', value: '24', change: '+2', trend: 'up', icon: '👥' },
    { title: 'Avg Performance', value: '4.2/5', change: '+0.3', trend: 'up', icon: '⭐' },
    { title: 'Team Satisfaction', value: '87%', change: '+5%', trend: 'up', icon: '😊' },
    { title: 'Active Projects', value: '8', change: '+1', trend: 'up', icon: '📁' },
  ];

  const performanceData = [
    { month: 'Jan', score: 3.8 },
    { month: 'Feb', score: 3.9 },
    { month: 'Mar', score: 4.0 },
    { month: 'Apr', score: 4.1 },
    { month: 'May', score: 4.15 },
    { month: 'Jun', score: 4.2 },
  ];

  const taskData = [
    { status: 'Completed', count: 156 },
    { status: 'In Progress', count: 42 },
    { status: 'Pending', count: 18 },
  ];

  return (
    <DashboardLayout onNavigate={onNavigate} userRole="manager" currentPage="manager-dashboard">
      <div className="dashboard-header">
        <div>
          <h1>Manager Dashboard</h1>
          <p className="dashboard-subtitle">Team performance and project insights</p>
        </div>
      </div>

      <div className="kpi-grid">
        {kpiData.map((kpi, index) => (
          <div key={index} className="kpi-card">
            <div className="kpi-icon">{kpi.icon}</div>
            <div className="kpi-content">
              <div className="kpi-title">{kpi.title}</div>
              <div className="kpi-value">{kpi.value}</div>
              <div className={`kpi-change ${kpi.trend}`}>
                {kpi.trend === 'up' ? '↑' : '↓'} {kpi.change}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Team Performance Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="month" stroke="#8b92b0" />
              <YAxis stroke="#8b92b0" domain={[0, 5]} />
              <Tooltip contentStyle={{ background: '#1a1f3a', border: '1px solid #00d4ff' }} />
              <Line type="monotone" dataKey="score" stroke="#00ff88" strokeWidth={3} dot={{ fill: '#00ff88', r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Task Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={taskData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="status" stroke="#8b92b0" />
              <YAxis stroke="#8b92b0" />
              <Tooltip contentStyle={{ background: '#1a1f3a', border: '1px solid #00d4ff' }} />
              <Bar dataKey="count" fill="#00d4ff" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ManagerDashboard;
