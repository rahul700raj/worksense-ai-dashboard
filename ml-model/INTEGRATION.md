# Integration Guide: ML Model + Dashboard

This guide shows how to integrate the ML prediction API with the WorkSense AI Dashboard.

## 🔗 Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│                     │         │                      │
│  React Dashboard    │ ◄─────► │  FastAPI ML Server   │
│  (Port 3000)        │  HTTP   │  (Port 8000)         │
│                     │         │                      │
└─────────────────────┘         └──────────────────────┘
         │                               │
         │                               │
         ▼                               ▼
   User Interface              XGBoost Model (.pkl)
```

## 🚀 Quick Integration

### Step 1: Start Both Services

**Terminal 1 - ML API:**
```bash
cd ml-model
python api.py
```

**Terminal 2 - Dashboard:**
```bash
npm start
```

### Step 2: Update Dashboard to Call API

Create a new service file: `src/services/mlService.js`

```javascript
// src/services/mlService.js
const API_BASE_URL = 'http://localhost:8000';

export const mlService = {
  // Predict single employee attrition
  async predictAttrition(employeeData) {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(employeeData)
    });
    
    if (!response.ok) {
      throw new Error('Prediction failed');
    }
    
    return await response.json();
  },

  // Batch prediction
  async predictBatch(employees) {
    const response = await fetch(`${API_BASE_URL}/predict/batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ employees })
    });
    
    if (!response.ok) {
      throw new Error('Batch prediction failed');
    }
    
    return await response.json();
  },

  // Get risk factor analysis
  async analyzeRiskFactors(employeeData) {
    const response = await fetch(`${API_BASE_URL}/analyze/risk-factors`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(employeeData)
    });
    
    if (!response.ok) {
      throw new Error('Risk analysis failed');
    }
    
    return await response.json();
  },

  // Get feature importance
  async getFeatureImportance() {
    const response = await fetch(`${API_BASE_URL}/features/importance`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch feature importance');
    }
    
    return await response.json();
  },

  // Health check
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await response.json();
  }
};
```

### Step 3: Update AttritionRisk Component

```javascript
// src/components/AttritionRisk.js
import React, { useState, useEffect } from 'react';
import DashboardLayout from './DashboardLayout';
import { mlService } from '../services/mlService';
import './Dashboard.css';

const AttritionRisk = ({ onNavigate, userRole }) => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    try {
      setLoading(true);
      
      // Sample employee data (replace with real data from your backend)
      const employees = [
        {
          salary_growth: 2.0,
          performance_score: 2.5,
          promotion_gap: 6,
          satisfaction_score: 4.0,
          work_hours: 60,
          overtime_frequency: 30
        },
        {
          salary_growth: 3.0,
          performance_score: 3.0,
          promotion_gap: 5,
          satisfaction_score: 5.0,
          work_hours: 55,
          overtime_frequency: 25
        },
        // Add more employees...
      ];

      const result = await mlService.predictBatch(employees);
      
      // Transform predictions to match UI format
      const transformedPredictions = result.predictions.map((pred, idx) => ({
        name: `Employee ${idx + 1}`, // Replace with real names
        role: 'Software Engineer', // Replace with real roles
        score: Math.round(pred.attrition_probability * 100),
        level: pred.risk_level.toLowerCase()
      }));

      setPredictions(transformedPredictions);
      setError(null);
    } catch (err) {
      setError('Failed to load predictions. Make sure ML API is running.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (level) => {
    if (level === 'critical' || level === 'high') return 'high';
    if (level === 'medium') return 'medium';
    return 'low';
  };

  if (loading) {
    return (
      <DashboardLayout onNavigate={onNavigate} userRole={userRole} currentPage="attrition-risk">
        <div className="dashboard-header">
          <h1>Loading predictions...</h1>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout onNavigate={onNavigate} userRole={userRole} currentPage="attrition-risk">
        <div className="dashboard-header">
          <h1>Error</h1>
          <p style={{ color: '#ff6b9d' }}>{error}</p>
          <button onClick={fetchPredictions} className="btn-primary">
            Retry
          </button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout onNavigate={onNavigate} userRole={userRole} currentPage="attrition-risk">
      <div className="dashboard-header">
        <div>
          <h1>AI-Powered Attrition Risk Analysis</h1>
          <p className="dashboard-subtitle">Real-time ML predictions</p>
        </div>
        <button onClick={fetchPredictions} className="btn-primary">
          Refresh Predictions
        </button>
      </div>

      <div className="insight-card">
        <div className="insight-header">
          <span className="insight-icon">⚠️</span>
          <h3 className="insight-title">Risk Overview</h3>
        </div>
        <p className="insight-content">
          AI model has analyzed {predictions.length} employees and identified attrition risks.
        </p>
        <div className="insight-metrics">
          <div className="metric-item">
            <div className="metric-label">High Risk</div>
            <div className="metric-value">
              {predictions.filter(p => p.level === 'high' || p.level === 'critical').length}
            </div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Medium Risk</div>
            <div className="metric-value">
              {predictions.filter(p => p.level === 'medium').length}
            </div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Low Risk</div>
            <div className="metric-value">
              {predictions.filter(p => p.level === 'low').length}
            </div>
          </div>
        </div>
      </div>

      <div className="chart-card">
        <h3>Employee Risk Scores</h3>
        <div className="risk-list">
          {predictions.map((employee, index) => (
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
```

### Step 4: Add CORS to API (Already Configured)

The API already has CORS enabled for all origins. In production, update to specific origins:

```python
# In api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🎯 Real-Time Integration Example

### Live Prediction on Employee Form

```javascript
// src/components/EmployeeForm.js
import React, { useState } from 'react';
import { mlService } from '../services/mlService';

const EmployeeForm = () => {
  const [formData, setFormData] = useState({
    salary_growth: 5.0,
    performance_score: 3.5,
    promotion_gap: 2,
    satisfaction_score: 7.0,
    work_hours: 45,
    overtime_frequency: 10
  });
  
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const result = await mlService.predictAttrition(formData);
      setPrediction(result);
    } catch (error) {
      console.error('Prediction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="employee-form">
      <h2>Employee Attrition Prediction</h2>
      
      {/* Form inputs */}
      <input
        type="number"
        value={formData.salary_growth}
        onChange={(e) => setFormData({...formData, salary_growth: parseFloat(e.target.value)})}
        placeholder="Salary Growth %"
      />
      
      {/* More inputs... */}
      
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Predicting...' : 'Predict Attrition Risk'}
      </button>

      {prediction && (
        <div className="prediction-result">
          <h3>Prediction Result</h3>
          <p>Risk Level: <strong>{prediction.risk_level}</strong></p>
          <p>Attrition Probability: <strong>{(prediction.attrition_probability * 100).toFixed(1)}%</strong></p>
          <p>Confidence: <strong>{(prediction.confidence * 100).toFixed(1)}%</strong></p>
        </div>
      )}
    </div>
  );
};
```

## 🔄 Data Flow

1. **User Input** → Dashboard collects employee data
2. **API Call** → Dashboard sends POST request to ML API
3. **Preprocessing** → API applies feature engineering
4. **Prediction** → XGBoost model makes prediction
5. **Response** → API returns prediction with probabilities
6. **Display** → Dashboard shows results to user

## 🚀 Production Deployment

### Option 1: Same Server
Deploy both on same server with Nginx reverse proxy:

```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;

    # Dashboard
    location / {
        proxy_pass http://localhost:3000;
    }

    # ML API
    location /api/ {
        proxy_pass http://localhost:8000/;
    }
}
```

### Option 2: Separate Servers
- **Dashboard**: Deploy on Vercel/Netlify
- **ML API**: Deploy on Railway/Render/AWS

Update API URL in dashboard:
```javascript
const API_BASE_URL = process.env.REACT_APP_ML_API_URL || 'http://localhost:8000';
```

## 📊 Advanced Features

### Real-Time Risk Monitoring

```javascript
// Auto-refresh predictions every 5 minutes
useEffect(() => {
  const interval = setInterval(() => {
    fetchPredictions();
  }, 5 * 60 * 1000); // 5 minutes

  return () => clearInterval(interval);
}, []);
```

### Risk Alerts

```javascript
const checkHighRiskEmployees = (predictions) => {
  const highRisk = predictions.filter(p => 
    p.attrition_probability > 0.75
  );
  
  if (highRisk.length > 0) {
    // Send notification
    showNotification(`${highRisk.length} employees at critical risk!`);
  }
};
```

## 🧪 Testing Integration

```javascript
// Test ML API connection
const testMLConnection = async () => {
  try {
    const health = await mlService.healthCheck();
    console.log('ML API Status:', health.status);
    return health.model_loaded;
  } catch (error) {
    console.error('ML API not available:', error);
    return false;
  }
};
```

## 📝 Environment Variables

Create `.env` file in dashboard root:

```env
REACT_APP_ML_API_URL=http://localhost:8000
REACT_APP_ML_API_TIMEOUT=30000
REACT_APP_ENABLE_ML_PREDICTIONS=true
```

## 🎉 Complete!

Your dashboard now has real-time ML predictions! The integration provides:

✅ Live attrition predictions  
✅ Risk factor analysis  
✅ Batch processing  
✅ Feature importance insights  
✅ Production-ready API  

---

**Need help? Check the ML model README or open an issue on GitHub!**
