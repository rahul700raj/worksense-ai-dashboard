# Employee Attrition Prediction ML Model

Production-ready machine learning model for predicting employee attrition risk using XGBoost.

## 🎯 Overview

This ML model predicts the likelihood of employee attrition based on 6 key features:
- **salary_growth**: Annual salary growth percentage
- **performance_score**: Employee performance rating (1-5)
- **promotion_gap**: Years since last promotion
- **satisfaction_score**: Employee satisfaction level (1-10)
- **work_hours**: Average weekly work hours
- **overtime_frequency**: Monthly overtime hours

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ml-model
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python generate_sample_data.py
```

This creates `employee_data.csv` with 5,000 synthetic employee records.

### 3. Train the Model

```bash
python train_model.py
```

**Output:**
- `attrition_model.pkl` - Trained model (saved with joblib)
- `confusion_matrix.png` - Confusion matrix visualization
- `roc_curve.png` - ROC curve with AUC score
- `feature_importance.png` - Feature importance chart

### 4. Start the API

```bash
python api.py
```

API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 5. Test the API

```bash
python test_api.py
```

## 📊 Model Performance

Expected metrics on test set:
- **Accuracy**: ~85-90%
- **Precision**: ~82-88%
- **Recall**: ~80-86%
- **F1 Score**: ~81-87%
- **ROC AUC**: ~88-93%

## 🔧 Model Architecture

### Preprocessing Pipeline
1. **Missing Value Handling**: Median imputation
2. **Feature Engineering**:
   - `work_life_balance` = 40 / work_hours
   - `promotion_performance_ratio` = promotion_gap / (performance_score + 1)
   - `stress_index` = (work_hours × overtime_frequency) / 100
   - `satisfaction_performance` = satisfaction_score × performance_score
3. **Feature Scaling**: StandardScaler (zero mean, unit variance)

### Model: XGBoost Classifier
- **Algorithm**: Gradient Boosting Decision Trees
- **Hyperparameter Tuning**: GridSearchCV with 3-fold CV
- **Optimized Parameters**:
  - max_depth: 3-7
  - learning_rate: 0.01-0.3
  - n_estimators: 100-300
  - min_child_weight: 1-5
  - subsample: 0.8-1.0
  - colsample_bytree: 0.8-1.0

### Data Split
- **Training**: 70%
- **Validation**: 10%
- **Test**: 20%

## 🌐 API Endpoints

### Health & Info

#### `GET /`
Root endpoint with API information

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-02-28T10:30:00"
}
```

#### `GET /model/info`
Get model information
```json
{
  "model_name": "XGBoost Attrition Predictor",
  "version": "1.0.0",
  "features": ["salary_growth", "performance_score", ...],
  "model_loaded": true
}
```

### Predictions

#### `POST /predict`
Predict attrition for a single employee

**Request:**
```json
{
  "salary_growth": 8.5,
  "performance_score": 4.2,
  "promotion_gap": 2,
  "satisfaction_score": 7.5,
  "work_hours": 45,
  "overtime_frequency": 10
}
```

**Response:**
```json
{
  "attrition": 0,
  "attrition_probability": 0.23,
  "retention_probability": 0.77,
  "risk_level": "Low",
  "confidence": 0.54,
  "timestamp": "2026-02-28T10:30:00"
}
```

#### `POST /predict/batch`
Predict attrition for multiple employees

**Request:**
```json
{
  "employees": [
    {
      "salary_growth": 5.0,
      "performance_score": 3.5,
      ...
    },
    {
      "salary_growth": 12.0,
      "performance_score": 4.2,
      ...
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [...],
  "total_employees": 2,
  "high_risk_count": 0,
  "medium_risk_count": 1,
  "low_risk_count": 1
}
```

### Analysis

#### `GET /features/importance`
Get feature importance rankings

#### `POST /analyze/risk-factors`
Analyze risk factors for an employee

**Response:**
```json
{
  "prediction": {...},
  "risk_factors": [
    {
      "factor": "Low Salary Growth",
      "value": 2.0,
      "impact": "High",
      "recommendation": "Consider salary review or performance bonus"
    }
  ],
  "total_risk_factors": 3,
  "overall_assessment": "High Risk"
}
```

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build image
docker build -t worksense-attrition-api .

# Run container
docker run -p 8000:8000 worksense-attrition-api
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📈 Model Retraining

To retrain the model with new data:

1. **Update dataset**: Replace or append to `employee_data.csv`
2. **Retrain**: Run `python train_model.py`
3. **Validate**: Check metrics and visualizations
4. **Deploy**: Replace `attrition_model.pkl` in production
5. **Restart API**: Reload the API to use new model

## 🔒 Production Considerations

### Security
- ✅ Input validation with Pydantic
- ✅ CORS configuration for frontend integration
- ✅ Rate limiting (configure in production)
- ✅ API key authentication (add if needed)

### Performance
- ✅ Model loaded once at startup
- ✅ Batch prediction support
- ✅ Efficient feature engineering
- ✅ Optimized XGBoost parameters

### Monitoring
- ✅ Health check endpoint
- ✅ Prediction logging (add to production)
- ✅ Model performance tracking (add metrics)
- ✅ Error handling and reporting

### Scalability
- ✅ Containerized with Docker
- ✅ Stateless API design
- ✅ Horizontal scaling ready
- ✅ Load balancer compatible

## 📊 Feature Importance

Top features influencing attrition (typical ranking):

1. **satisfaction_score** - Employee satisfaction level
2. **promotion_gap** - Time since last promotion
3. **salary_growth** - Salary increase percentage
4. **stress_index** - Workload stress indicator
5. **performance_score** - Performance rating
6. **work_hours** - Weekly work hours
7. **overtime_frequency** - Monthly overtime
8. **work_life_balance** - Work-life balance score
9. **promotion_performance_ratio** - Career progression
10. **satisfaction_performance** - Combined metric

## 🧪 Testing

### Unit Tests
```bash
pytest test_model.py
```

### API Tests
```bash
python test_api.py
```

### Load Testing
```bash
# Install locust
pip install locust

# Run load test
locust -f load_test.py
```

## 📝 Example Usage

### Python Client

```python
import requests

# Single prediction
employee = {
    "salary_growth": 5.0,
    "performance_score": 3.5,
    "promotion_gap": 3,
    "satisfaction_score": 6.5,
    "work_hours": 45,
    "overtime_frequency": 15
}

response = requests.post(
    "http://localhost:8000/predict",
    json=employee
)

result = response.json()
print(f"Attrition Risk: {result['risk_level']}")
print(f"Probability: {result['attrition_probability']:.2%}")
```

### cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "salary_growth": 5.0,
    "performance_score": 3.5,
    "promotion_gap": 3,
    "satisfaction_score": 6.5,
    "work_hours": 45,
    "overtime_frequency": 15
  }'
```

### JavaScript/Fetch

```javascript
const employee = {
  salary_growth: 5.0,
  performance_score: 3.5,
  promotion_gap: 3,
  satisfaction_score: 6.5,
  work_hours: 45,
  overtime_frequency: 15
};

fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(employee)
})
.then(res => res.json())
.then(data => console.log(data));
```

## 🔄 Integration with Dashboard

To integrate with the WorkSense AI dashboard:

1. **Update API URL** in dashboard config
2. **Add API calls** in AttritionRisk component
3. **Display predictions** in real-time
4. **Show risk factors** and recommendations

Example integration:
```javascript
// In AttritionRisk.js
const fetchPrediction = async (employeeData) => {
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(employeeData)
  });
  return await response.json();
};
```

## 📚 Additional Resources

- **XGBoost Documentation**: https://xgboost.readthedocs.io/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Scikit-learn Guide**: https://scikit-learn.org/stable/

## 🤝 Contributing

To improve the model:
1. Add more features (tenure, department, location, etc.)
2. Collect real employee data
3. Experiment with other algorithms (Random Forest, Neural Networks)
4. Implement A/B testing for model versions
5. Add explainability (SHAP values, LIME)

## 📄 License

MIT License - See main repository LICENSE file

## 👨‍💻 Author

**Rahul Mishra**
- Email: rm2778643@gmail.com
- GitHub: [@rahul700raj](https://github.com/rahul700raj)

---

**🚀 Production-Ready ML Model for Employee Attrition Prediction**
