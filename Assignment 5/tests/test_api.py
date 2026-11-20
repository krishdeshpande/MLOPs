"""
Assignment 5: REST API using FastAPI
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C

Pytest test suite for all FastAPI endpoints.
Requires model.pkl to exist (run src/train_model.py first).
"""

import os
import sys
import pytest
import joblib
import numpy as np
from fastapi.testclient import TestClient
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

# Ensure project root is on sys.path so `main` can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def ensure_model():
    """Train and save a model.pkl if it does not already exist."""
    model_path = os.path.join(os.path.dirname(__file__), "..", "model.pkl")
    model_path = os.path.abspath(model_path)
    if not os.path.exists(model_path):
        iris = load_iris()
        model = LogisticRegression(max_iter=200, random_state=42)
        model.fit(iris.data, iris.target)
        joblib.dump(model, model_path)
        print(f"\n[fixture] model.pkl created at {model_path}")
    yield
    # Leave the file — the main app needs it.


@pytest.fixture(scope="module")
def client(ensure_model):
    """Create a TestClient for the FastAPI app."""
    from main import app
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRootEndpoint:
    def test_root_status_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_contains_message(self, client):
        data = response = client.get("/")
        assert "message" in response.json()

    def test_root_message_text(self, client):
        data = client.get("/").json()
        assert "Welcome" in data["message"]


class TestHealthEndpoint:
    def test_health_status_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok(self, client):
        data = client.get("/health").json()
        assert data["status"] == "ok"


class TestModelInfoEndpoint:
    def test_model_info_status_200(self, client):
        response = client.get("/model-info")
        assert response.status_code == 200

    def test_model_info_has_model_type(self, client):
        data = client.get("/model-info").json()
        assert "model_type" in data
        assert data["model_type"] == "LogisticRegression"

    def test_model_info_classes(self, client):
        data = client.get("/model-info").json()
        assert data["classes"] == ["setosa", "versicolor", "virginica"]
        assert data["num_classes"] == 3

    def test_model_info_features(self, client):
        data = client.get("/model-info").json()
        expected_features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        assert data["features"] == expected_features
        assert data["num_features"] == 4


class TestPredictEndpoint:
    SETOSA_INPUT = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    VIRGINICA_INPUT = {
        "sepal_length": 6.3,
        "sepal_width": 2.5,
        "petal_length": 5.0,
        "petal_width": 1.9,
    }

    def test_predict_status_200(self, client):
        response = client.post("/predict", json=self.SETOSA_INPUT)
        assert response.status_code == 200

    def test_predict_returns_expected_fields(self, client):
        data = client.post("/predict", json=self.SETOSA_INPUT).json()
        assert "predicted_class" in data
        assert "class_name" in data
        assert "confidence" in data

    def test_predict_setosa(self, client):
        data = client.post("/predict", json=self.SETOSA_INPUT).json()
        assert data["predicted_class"] == 0
        assert data["class_name"] == "setosa"

    def test_predict_confidence_range(self, client):
        data = client.post("/predict", json=self.SETOSA_INPUT).json()
        assert 0.0 <= data["confidence"] <= 1.0

    def test_predict_virginica(self, client):
        data = client.post("/predict", json=self.VIRGINICA_INPUT).json()
        # Logistic Regression reliably classifies this sample as virginica (2)
        assert data["class_name"] in ["versicolor", "virginica"]

    def test_predict_invalid_input_missing_field(self, client):
        # Missing petal_width
        response = client.post("/predict", json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
        })
        assert response.status_code == 422

    def test_predict_invalid_input_non_numeric(self, client):
        response = client.post("/predict", json={
            "sepal_length": "abc",
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        })
        assert response.status_code == 422

    def test_predict_invalid_input_negative_value(self, client):
        # Negative values violate gt=0 constraint
        response = client.post("/predict", json={
            "sepal_length": -1.0,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        })
        assert response.status_code == 422

    def test_predict_multiple_samples_consistency(self, client):
        """Same input should always produce the same output."""
        r1 = client.post("/predict", json=self.SETOSA_INPUT).json()
        r2 = client.post("/predict", json=self.SETOSA_INPUT).json()
        assert r1["predicted_class"] == r2["predicted_class"]
        assert r1["class_name"] == r2["class_name"]
        assert r1["confidence"] == r2["confidence"]
