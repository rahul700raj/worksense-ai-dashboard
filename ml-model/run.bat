@echo off
REM WorkSense AI - ML Model Quick Start Script (Windows)
REM This script sets up and runs the complete ML pipeline

echo ==========================================
echo 🚀 WorkSense AI - ML Model Setup
echo ==========================================
echo.

REM Check Python version
echo 📋 Checking Python version...
python --version
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Generate sample data
echo 📊 Generating sample employee data...
python generate_sample_data.py
echo ✅ Sample data generated
echo.

REM Train model
echo 🤖 Training ML model...
python train_model.py
echo ✅ Model trained successfully
echo.

REM Start API
echo 🌐 Starting FastAPI server...
echo    API will be available at: http://localhost:8000
echo    Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

python api.py
