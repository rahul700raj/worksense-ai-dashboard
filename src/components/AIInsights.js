import React from 'react';
import DashboardLayout from './DashboardLayout';
import './Dashboard.css';

const AIInsights = ({ onNavigate, userRole }) => {
  const insights = [
    {
      icon: '🤖',
      title: 'Hiring Forecast',
      content: 'Based on current growth trends and project pipeline, we recommend hiring 15-20 additional engineers in Q3 to meet demand.',
      metrics: [
        { label: 'Recommended Hires', value: '15-20' },
        { label: 'Confidence', value: '87%' },
        { label: 'Timeline', value: 'Q3 2026' }
      ]
    },
    {
      icon: '📈',
      title: 'Performance Prediction',
      content: 'AI models predict a 12% improvement in team productivity if recommended training programs are implemented.',
      metrics: [
        { label: 'Expected Improvement', value: '+12%' },
        { label: 'Investment Required', value: '$45K' },
        { label: 'ROI', value: '340%' }
      ]
    },
    {
      icon: '⚡',
      title: 'Retention Strategy',
      content: 'Implementing flexible work policies and career development programs could reduce attrition by 35% in high-risk segments.',
      metrics: [
        { label: 'Attrition Reduction', value: '-35%' },
        { label: 'Affected Employees', value: '47' },
        { label: 'Cost Savings', value: '$280K' }
      ]
    }
  ];

  return (
    <DashboardLayout onNavigate={onNavigate} userRole={userRole} currentPage="ai-insights">
      <div className="dashboard-header">
        <div>
          <h1>AI-Powered Insights</h1>
          <p className="dashboard-subtitle">Machine learning predictions and recommendations</p>
        </div>
      </div>

      {insights.map((insight, index) => (
        <div key={index} className="insight-card">
          <div className="insight-header">
            <span className="insight-icon">{insight.icon}</span>
            <h3 className="insight-title">{insight.title}</h3>
          </div>
          <p className="insight-content">{insight.content}</p>
          <div className="insight-metrics">
            {insight.metrics.map((metric, idx) => (
              <div key={idx} className="metric-item">
                <div className="metric-label">{metric.label}</div>
                <div className="metric-value">{metric.value}</div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </DashboardLayout>
  );
};

export default AIInsights;
