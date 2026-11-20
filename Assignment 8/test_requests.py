"""
Assignment 8: Test script to generate prediction requests for Prometheus monitoring
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | AIDS Div-C
"""

import requests
import time
import random

API_URL = "http://localhost:8000"

# Sample Iris data for predictions
samples = [
    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
    {"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 4.7, "petal_width": 1.6},
    {"sepal_length": 7.2, "sepal_width": 3.0, "petal_length": 5.8, "petal_width": 1.6},
    {"sepal_length": 5.5, "sepal_width": 2.4, "petal_length": 3.8, "petal_width": 1.1},
    {"sepal_length": 6.7, "sepal_width": 3.1, "petal_length": 5.6, "petal_width": 2.4},
]

print("Sending 20 prediction requests to test monitoring...")
print(f"API URL: {API_URL}")
print("-" * 50)

success = 0
failed  = 0

for i in range(20):
    sample = random.choice(samples)
    try:
        response = requests.post(f"{API_URL}/predict", json=sample, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"[{i+1:02d}] ✓ Predicted: {result['class_name']} (confidence: {result['confidence']:.3f})")
            success += 1
        else:
            print(f"[{i+1:02d}] ✗ Error {response.status_code}: {response.text}")
            failed += 1
    except Exception as e:
        print(f"[{i+1:02d}] ✗ Connection error: {e}")
        failed += 1
    time.sleep(0.5)

print("-" * 50)
print(f"Results: {success} successful, {failed} failed")
print(f"\nView Prometheus metrics: {API_URL}/metrics")
print(f"Prometheus dashboard:    http://localhost:9090")
print(f"Grafana dashboard:       http://localhost:3000  (admin/admin)")
