import React from 'react';
import DashboardLayout from './DashboardLayout';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Dashboard.css';

const HRDashboard = ({ onNavigate }) => {
  const kpiData = [
    { title: 'Total Employees', value: '1,247', change: '+12%', trend: 'up', icon: '👥' },
    { title: 'Attrition Rate', value: '8.3%', change: '-2.1%', trend: 'down', icon: '📉' },
    { title: 'Avg. Tenure', value: '3.2 yrs', change: '+0.4', trend: 'up', icon: '⏱️' },
    { title: 'Open Positions', value: '47', change: '+8', trend: 'up', icon: '📋' },
  ];

  const headcountData = [
    { month: 'Jan', count: 1180 },
    { month: 'Feb', count: 1195 },
    { month: 'Mar', count: 1210 },
    { month: 'Apr', count: 1225 },
    { month: 'May', count: 1235 },
    { month: 'Jun', count: 1247 },
  ];

  const departmentData = [
    { name: 'Engineering', value: 487, color: '#00d4ff' },
    { name: 'Sales', value: 312, color: '#00ff88' },
    { name: 'Marketing', value: 156, color: '#ff6b9d' },
    { name: 'HR', value: 89, color: '#ffd93d' },
    { name: 'Finance', value: 103, color: '#a78bfa' },
    { name: 'Operations', value: 100, color: '#fb923c' },
  ];

  const performanceData = [
    { category: 'Exceeds', count: 312 },
    { category: 'Meets', count: 789 },
    { category: 'Needs Improvement', count: 146 },
  ];

  return (
    <DashboardLayout onNavigate={onNavigate} userRole="hr" currentPage="hr-dashboard">
      <div className="dashboard-header">
        <div>
          <h1>HR Analytics Dashboard</h1>
          <p className="dashboard-subtitle">Comprehensive workforce insights and metrics</p>
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
          <h3>Headcount Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={headcountData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="month" stroke="#8b92b0" />
              <YAxis stroke="#8b92b0" />
              <Tooltip contentStyle={{ background: '#1a1f3a', border: '1px solid #00d4ff' }} />
              <Line type="monotone" dataKey="count" stroke="#00d4ff" strokeWidth={3} dot={{ fill: '#00d4ff', r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Department Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={departmentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {departmentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: '#1a1f3a', border: '1px solid #00d4ff' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card full-width">
          <h3>Performance Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="category" stroke="#8b92b0" />
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

export default HRDashboard;
