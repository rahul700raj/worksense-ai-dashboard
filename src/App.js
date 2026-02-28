import React, { useState } from 'react';
import './App.css';
import Login from './components/Login';
import Signup from './components/Signup';
import HRDashboard from './components/HRDashboard';
import ManagerDashboard from './components/ManagerDashboard';
import EmployeeDashboard from './components/EmployeeDashboard';
import AIInsights from './components/AIInsights';
import AttritionRisk from './components/AttritionRisk';
import SkillGapAnalysis from './components/SkillGapAnalysis';

function App() {
  const [currentPage, setCurrentPage] = useState('login');
  const [userRole, setUserRole] = useState(null);

  const handleLogin = (role) => {
    setUserRole(role);
    if (role === 'hr') setCurrentPage('hr-dashboard');
    else if (role === 'manager') setCurrentPage('manager-dashboard');
    else setCurrentPage('employee-dashboard');
  };

  const renderPage = () => {
    switch(currentPage) {
      case 'login':
        return <Login onLogin={handleLogin} onSignup={() => setCurrentPage('signup')} />;
      case 'signup':
        return <Signup onBack={() => setCurrentPage('login')} />;
      case 'hr-dashboard':
        return <HRDashboard onNavigate={setCurrentPage} />;
      case 'manager-dashboard':
        return <ManagerDashboard onNavigate={setCurrentPage} />;
      case 'employee-dashboard':
        return <EmployeeDashboard onNavigate={setCurrentPage} />;
      case 'ai-insights':
        return <AIInsights onNavigate={setCurrentPage} userRole={userRole} />;
      case 'attrition-risk':
        return <AttritionRisk onNavigate={setCurrentPage} userRole={userRole} />;
      case 'skill-gap':
        return <SkillGapAnalysis onNavigate={setCurrentPage} userRole={userRole} />;
      default:
        return <Login onLogin={handleLogin} onSignup={() => setCurrentPage('signup')} />;
    }
  };

  return (
    <div className="App">
      {renderPage()}
    </div>
  );
}

export default App;
