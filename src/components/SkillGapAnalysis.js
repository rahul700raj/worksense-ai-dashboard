import React from 'react';
import DashboardLayout from './DashboardLayout';
import './Dashboard.css';

const SkillGapAnalysis = ({ onNavigate, userRole }) => {
  const departments = [
    {
      name: 'Engineering',
      skills: [
        { name: 'React/Frontend', current: 75, target: 90 },
        { name: 'Cloud Architecture', current: 60, target: 85 },
        { name: 'DevOps', current: 55, target: 80 },
        { name: 'AI/ML', current: 40, target: 75 }
      ]
    },
    {
      name: 'Product',
      skills: [
        { name: 'Data Analysis', current: 70, target: 85 },
        { name: 'UX Research', current: 65, target: 80 },
        { name: 'Agile/Scrum', current: 80, target: 90 },
        { name: 'Product Strategy', current: 60, target: 85 }
      ]
    },
    {
      name: 'Sales',
      skills: [
        { name: 'Enterprise Sales', current: 75, target: 90 },
        { name: 'CRM Tools', current: 85, target: 95 },
        { name: 'Negotiation', current: 70, target: 85 },
        { name: 'Market Analysis', current: 55, target: 75 }
      ]
    }
  ];

  return (
    <DashboardLayout onNavigate={onNavigate} userRole={userRole} currentPage="skill-gap">
      <div className="dashboard-header">
        <div>
          <h1>Skill Gap Analysis</h1>
          <p className="dashboard-subtitle">Identify training needs and development opportunities</p>
        </div>
      </div>

      <div className="insight-card">
        <div className="insight-header">
          <span className="insight-icon">📊</span>
          <h3 className="insight-title">Analysis Summary</h3>
        </div>
        <p className="insight-content">
          Based on current skill assessments and future business needs, we've identified key gaps across departments. 
          Recommended training programs could close these gaps within 6-9 months.
        </p>
        <div className="insight-metrics">
          <div className="metric-item">
            <div className="metric-label">Avg Skill Level</div>
            <div className="metric-value">67%</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Target Level</div>
            <div className="metric-value">84%</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Gap to Close</div>
            <div className="metric-value">17%</div>
          </div>
        </div>
      </div>

      <div className="skill-grid">
        {departments.map((dept, index) => (
          <div key={index} className="skill-card">
            <h4>{dept.name}</h4>
            {dept.skills.map((skill, idx) => (
              <div key={idx} className="skill-bar">
                <div className="skill-bar-header">
                  <span className="skill-name">{skill.name}</span>
                  <span className="skill-percentage">{skill.current}% / {skill.target}%</span>
                </div>
                <div className="skill-bar-track">
                  <div 
                    className="skill-bar-fill" 
                    style={{ width: `${(skill.current / skill.target) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
};

export default SkillGapAnalysis;
