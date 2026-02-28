"""
API Testing Script
Test all endpoints of the Attrition Prediction API
"""
import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"


def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print(f"{'='*60}\n")


def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    return response.status_code == 200


def test_health():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_model_info():
    """Test model info endpoint"""
    response = requests.get(f"{BASE_URL}/model/info")
    print_response("Model Info", response)
    return response.status_code == 200


def test_single_prediction():
    """Test single employee prediction"""
    # High risk employee
    high_risk_employee = {
        "salary_growth": 2.0,
        "performance_score": 2.5,
        "promotion_gap": 6,
        "satisfaction_score": 4.0,
        "work_hours": 60,
        "overtime_frequency": 30
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=high_risk_employee
    )
    print_response("Single Prediction (High Risk)", response)
    
    # Low risk employee
    low_risk_employee = {
        "salary_growth": 15.0,
        "performance_score": 4.5,
        "promotion_gap": 1,
        "satisfaction_score": 9.0,
        "work_hours": 40,
        "overtime_frequency": 5
    }
    
    response2 = requests.post(
        f"{BASE_URL}/predict",
        json=low_risk_employee
    )
    print_response("Single Prediction (Low Risk)", response2)
    
    return response.status_code == 200 and response2.status_code == 200


def test_batch_prediction():
    """Test batch prediction"""
    batch_request = {
        "employees": [
            {
                "salary_growth": 5.0,
                "performance_score": 3.5,
                "promotion_gap": 3,
                "satisfaction_score": 6.5,
                "work_hours": 45,
                "overtime_frequency": 15
            },
            {
                "salary_growth": 12.0,
                "performance_score": 4.2,
                "promotion_gap": 1,
                "satisfaction_score": 8.5,
                "work_hours": 42,
                "overtime_frequency": 8
            },
            {
                "salary_growth": 1.0,
                "performance_score": 2.8,
                "promotion_gap": 5,
                "satisfaction_score": 5.0,
                "work_hours": 55,
                "overtime_frequency": 25
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/predict/batch",
        json=batch_request
    )
    print_response("Batch Prediction (3 Employees)", response)
    return response.status_code == 200


def test_feature_importance():
    """Test feature importance endpoint"""
    response = requests.get(f"{BASE_URL}/features/importance")
    print_response("Feature Importance", response)
    return response.status_code == 200


def test_risk_analysis():
    """Test risk factor analysis"""
    employee = {
        "salary_growth": 3.0,
        "performance_score": 3.0,
        "promotion_gap": 4,
        "satisfaction_score": 5.5,
        "work_hours": 52,
        "overtime_frequency": 22
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze/risk-factors",
        json=employee
    )
    print_response("Risk Factor Analysis", response)
    return response.status_code == 200


def test_invalid_input():
    """Test API validation with invalid input"""
    invalid_employee = {
        "salary_growth": 100.0,  # Invalid: too high
        "performance_score": 6.0,  # Invalid: out of range
        "promotion_gap": -1,  # Invalid: negative
        "satisfaction_score": 11.0,  # Invalid: out of range
        "work_hours": 100,  # Invalid: too high
        "overtime_frequency": -5  # Invalid: negative
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=invalid_employee
    )
    print_response("Invalid Input Test (Should Fail)", response)
    return response.status_code == 422  # Validation error


def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("🚀 STARTING API TESTS")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API is running: python ml-model/api.py")
    print("="*60 + "\n")
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Model Info", test_model_info),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Feature Importance", test_feature_importance),
        ("Risk Analysis", test_risk_analysis),
        ("Invalid Input Validation", test_invalid_input)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error in {test_name}: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"{'='*60}\n")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Please start the API first: python ml-model/api.py")
        print("\n")
        exit(1)
