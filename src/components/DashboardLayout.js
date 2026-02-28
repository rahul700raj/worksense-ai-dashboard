import React, { useState } from 'react';
import './DashboardLayout.css';

const DashboardLayout = ({ children, onNavigate, userRole, currentPage }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const menuItems = {
    hr: [
      { id: 'hr-dashboard', icon: '📊', label: 'Dashboard' },
      { id: 'ai-insights', icon: '🤖', label: 'AI Insights' },
      { id: 'attrition-risk', icon: '⚠️', label: 'Attrition Risk' },
      { id: 'skill-gap', icon: '📈', label: 'Skill Gap Analysis' },
    ],
    manager: [
      { id: 'manager-dashboard', icon: '📊', label: 'Dashboard' },
      { id: 'ai-insights', icon: '🤖', label: 'AI Insights' },
      { id: 'attrition-risk', icon: '⚠️', label: 'Team Health' },
      { id: 'skill-gap', icon: '📈', label: 'Skill Development' },
    ],
    employee: [
      { id: 'employee-dashboard', icon: '📊', label: 'Dashboard' },
      { id: 'ai-insights', icon: '🤖', label: 'Career Insights' },
      { id: 'skill-gap', icon: '📈', label: 'My Skills' },
    ]
  };

  const items = menuItems[userRole] || menuItems.hr;

  return (
    <div className="dashboard-layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="sidebar-logo-icon">WS</div>
            {sidebarOpen && <span>WorkSense AI</span>}
          </div>
        </div>
        <nav className="sidebar-nav">
          {items.map(item => (
            <button
              key={item.id}
              className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
              onClick={() => onNavigate(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && <span className="nav-label">{item.label}</span>}
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <button className="nav-item" onClick={() => onNavigate('login')}>
            <span className="nav-icon">🚪</span>
            {sidebarOpen && <span className="nav-label">Logout</span>}
          </button>
        </div>
      </aside>
      <div className="main-content">
        <header className="top-header">
          <button className="menu-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
            ☰
          </button>
          <div className="header-right">
            <div className="user-profile">
              <div className="user-avatar">
                {userRole === 'hr' ? 'HR' : userRole === 'manager' ? 'MG' : 'EM'}
              </div>
              <span className="user-name">
                {userRole === 'hr' ? 'HR Admin' : userRole === 'manager' ? 'Manager' : 'Employee'}
              </span>
            </div>
          </div>
        </header>
        <main className="content-area">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
