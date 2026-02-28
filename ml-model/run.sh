#!/bin/bash

# WorkSense AI - ML Model Quick Start Script
# This script sets up and runs the complete ML pipeline

echo "=========================================="
echo "🚀 WorkSense AI - ML Model Setup"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Generate sample data
echo "📊 Generating sample employee data..."
python3 generate_sample_data.py
echo "✅ Sample data generated"
echo ""

# Train model
echo "🤖 Training ML model..."
python3 train_model.py
echo "✅ Model trained successfully"
echo ""

# Start API
echo "🌐 Starting FastAPI server..."
echo "   API will be available at: http://localhost:8000"
echo "   Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 api.py
