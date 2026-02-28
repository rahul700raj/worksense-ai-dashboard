"""
FastAPI Production API for Employee Attrition Prediction
Provides REST endpoints for real-time predictions
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="WorkSense AI - Attrition Prediction API",
    description="Production-ready ML API for predicting employee attrition risk",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model_data = None


class EmployeeFeatures(BaseModel):
    """Input schema for employee features"""
    salary_growth: float = Field(..., ge=-10, le=50, description="Annual salary growth percentage")
    performance_score: float = Field(..., ge=1, le=5, description="Performance rating (1-5)")
    promotion_gap: int = Field(..., ge=0, le=20, description="Years since last promotion")
    satisfaction_score: float = Field(..., ge=1, le=10, description="Employee satisfaction (1-10)")
    work_hours: float = Field(..., ge=20, le=80, description="Average weekly work hours")
    overtime_frequency: float = Field(..., ge=0, le=60, description="Monthly overtime hours")
    
    @validator('salary_growth')
    def validate_salary_growth(cls, v):
        if v < -10 or v > 50:
            raise ValueError('Salary growth must be between -10% and 50%')
        return v
    
    @validator('performance_score')
    def validate_performance(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Performance score must be between 1 and 5')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "salary_growth": 8.5,
                "performance_score": 4.2,
                "promotion_gap": 2,
                "satisfaction_score": 7.5,
                "work_hours": 45,
                "overtime_frequency": 10
            }
        }


class BatchPredictionRequest(BaseModel):
    """Batch prediction request schema"""
    employees: List[EmployeeFeatures]


class PredictionResponse(BaseModel):
    """Prediction response schema"""
    attrition: int = Field(..., description="Predicted attrition (0=Retained, 1=Attrition)")
    attrition_probability: float = Field(..., description="Probability of attrition (0-1)")
    retention_probability: float = Field(..., description="Probability of retention (0-1)")
    risk_level: str = Field(..., description="Risk level: Low, Medium, High, Critical")
    confidence: float = Field(..., description="Model confidence (0-1)")
    timestamp: str = Field(..., description="Prediction timestamp")


class BatchPredictionResponse(BaseModel):
    """Batch prediction response schema"""
    predictions: List[PredictionResponse]
    total_employees: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int


class ModelInfo(BaseModel):
    """Model information schema"""
    model_name: str
    version: str
    features: List[str]
    model_loaded: bool
    last_trained: Optional[str] = None


def load_model():
    """Load the trained model on startup"""
    global model_data
    try:
        model_data = joblib.load('ml-model/attrition_model.pkl')
        print("✅ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False


def engineer_features(features: dict) -> pd.DataFrame:
    """Apply feature engineering"""
    df = pd.DataFrame([features])
    
    # Same feature engineering as training
    df['work_life_balance'] = 40 / df['work_hours']
    df['promotion_performance_ratio'] = df['promotion_gap'] / (df['performance_score'] + 1)
    df['stress_index'] = (df['work_hours'] * df['overtime_frequency']) / 100
    df['satisfaction_performance'] = df['satisfaction_score'] * df['performance_score']
    
    return df


def get_risk_level(probability: float) -> str:
    """Determine risk level based on probability"""
    if probability >= 0.75:
        return "Critical"
    elif probability >= 0.5:
        return "High"
    elif probability >= 0.3:
        return "Medium"
    else:
        return "Low"


@app.on_event("startup")
async def startup_event():
    """Load model on API startup"""
    print("\n" + "="*60)
    print("🚀 Starting WorkSense AI Attrition Prediction API")
    print("="*60)
    load_model()
    print("="*60 + "\n")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "WorkSense AI - Attrition Prediction API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_data is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/model/info", response_model=ModelInfo, tags=["Model"])
async def get_model_info():
    """Get model information"""
    if model_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    return {
        "model_name": "XGBoost Attrition Predictor",
        "version": "1.0.0",
        "features": model_data['feature_names'],
        "model_loaded": True,
        "last_trained": None  # Add timestamp if available
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_attrition(employee: EmployeeFeatures):
    """
    Predict attrition risk for a single employee
    
    Returns:
    - attrition: 0 (Retained) or 1 (Attrition)
    - attrition_probability: Probability of leaving (0-1)
    - retention_probability: Probability of staying (0-1)
    - risk_level: Low, Medium, High, or Critical
    - confidence: Model confidence score
    """
    if model_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please contact administrator."
        )
    
    try:
        # Convert to dict and engineer features
        features_dict = employee.dict()
        features_df = engineer_features(features_dict)
        
        # Ensure correct feature order
        features_df = features_df[model_data['feature_names']]
        
        # Scale features
        features_scaled = model_data['scaler'].transform(features_df)
        
        # Predict
        prediction = model_data['model'].predict(features_scaled)[0]
        probabilities = model_data['model'].predict_proba(features_scaled)[0]
        
        attrition_prob = float(probabilities[1])
        retention_prob = float(probabilities[0])
        
        # Calculate confidence (distance from 0.5)
        confidence = abs(attrition_prob - 0.5) * 2
        
        return {
            "attrition": int(prediction),
            "attrition_probability": attrition_prob,
            "retention_probability": retention_prob,
            "risk_level": get_risk_level(attrition_prob),
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict attrition risk for multiple employees
    
    Useful for bulk analysis and reporting
    """
    if model_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        predictions = []
        risk_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        
        for employee in request.employees:
            # Get prediction for each employee
            result = await predict_attrition(employee)
            predictions.append(result)
            risk_counts[result.risk_level] += 1
        
        return {
            "predictions": predictions,
            "total_employees": len(predictions),
            "high_risk_count": risk_counts["High"] + risk_counts["Critical"],
            "medium_risk_count": risk_counts["Medium"],
            "low_risk_count": risk_counts["Low"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction error: {str(e)}"
        )


@app.get("/features/importance", tags=["Model"])
async def get_feature_importance():
    """Get feature importance rankings"""
    if model_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    importance_df = model_data['feature_importance']
    
    return {
        "features": importance_df.to_dict('records'),
        "top_5": importance_df.head(5).to_dict('records')
    }


@app.post("/analyze/risk-factors", tags=["Analysis"])
async def analyze_risk_factors(employee: EmployeeFeatures):
    """
    Analyze which factors contribute most to attrition risk
    
    Returns detailed breakdown of risk factors
    """
    if model_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    features_dict = employee.dict()
    
    # Analyze each factor
    risk_factors = []
    
    # Salary growth
    if features_dict['salary_growth'] < 5:
        risk_factors.append({
            "factor": "Low Salary Growth",
            "value": features_dict['salary_growth'],
            "impact": "High",
            "recommendation": "Consider salary review or performance bonus"
        })
    
    # Performance score
    if features_dict['performance_score'] < 3:
        risk_factors.append({
            "factor": "Low Performance Score",
            "value": features_dict['performance_score'],
            "impact": "Medium",
            "recommendation": "Provide performance improvement plan and mentoring"
        })
    
    # Promotion gap
    if features_dict['promotion_gap'] > 3:
        risk_factors.append({
            "factor": "Long Promotion Gap",
            "value": features_dict['promotion_gap'],
            "impact": "High",
            "recommendation": "Review career progression opportunities"
        })
    
    # Satisfaction
    if features_dict['satisfaction_score'] < 6:
        risk_factors.append({
            "factor": "Low Satisfaction",
            "value": features_dict['satisfaction_score'],
            "impact": "Critical",
            "recommendation": "Conduct one-on-one meeting to address concerns"
        })
    
    # Work hours
    if features_dict['work_hours'] > 50:
        risk_factors.append({
            "factor": "High Work Hours",
            "value": features_dict['work_hours'],
            "impact": "Medium",
            "recommendation": "Review workload distribution and work-life balance"
        })
    
    # Overtime
    if features_dict['overtime_frequency'] > 20:
        risk_factors.append({
            "factor": "Excessive Overtime",
            "value": features_dict['overtime_frequency'],
            "impact": "Medium",
            "recommendation": "Reduce overtime requirements or provide compensation"
        })
    
    # Get prediction
    prediction = await predict_attrition(employee)
    
    return {
        "prediction": prediction,
        "risk_factors": risk_factors,
        "total_risk_factors": len(risk_factors),
        "overall_assessment": "High Risk" if len(risk_factors) >= 3 else "Moderate Risk" if len(risk_factors) >= 2 else "Low Risk"
    }


if __name__ == "__main__":
    # Run the API server
    print("\n🚀 Starting FastAPI server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("📊 Alternative Docs: http://localhost:8000/redoc")
    print("\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
