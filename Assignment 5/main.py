"""
Assignment 5: REST API using FastAPI
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C

FastAPI application serving a trained Iris classifier.
"""

import os
from contextlib import asynccontextmanager
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.linear_model import LogisticRegression

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class IrisInput(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Sepal length in cm")
    sepal_width: float  = Field(..., gt=0, description="Sepal width in cm")
    petal_length: float = Field(..., gt=0, description="Petal length in cm")
    petal_width: float  = Field(..., gt=0, description="Petal width in cm")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    predicted_class: int
    class_name: str
    confidence: float


class HealthResponse(BaseModel):
    status: str


class ModelInfoResponse(BaseModel):
    model_type: str
    classes: List[str]
    features: List[str]
    num_features: int
    num_classes: int


# ---------------------------------------------------------------------------
# Application State
# ---------------------------------------------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

IRIS_CLASS_NAMES = ["setosa", "versicolor", "virginica"]
IRIS_FEATURE_NAMES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

# Global model holder
app_state: dict = {}


# ---------------------------------------------------------------------------
# Lifespan (loads model once at startup)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML model on startup; clean up on shutdown."""
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(
            f"model.pkl not found at {MODEL_PATH}. "
            "Run `python src/train_model.py` first."
        )
    app_state["model"] = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
    yield
    app_state.clear()
    print("Model unloaded.")


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Iris Classifier API",
    description="REST API for Iris flower classification using Logistic Regression.",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", summary="Root", tags=["General"])
def root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to the Iris Classifier API!",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict",
    }


@app.get("/health", response_model=HealthResponse, summary="Health Check", tags=["General"])
def health_check():
    """Returns service health status."""
    if "model" not in app_state:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return HealthResponse(status="ok")


@app.get("/model-info", response_model=ModelInfoResponse, summary="Model Information", tags=["Model"])
def model_info():
    """Returns metadata about the loaded ML model."""
    if "model" not in app_state:
        raise HTTPException(status_code=503, detail="Model not loaded")

    model: LogisticRegression = app_state["model"]
    return ModelInfoResponse(
        model_type=type(model).__name__,
        classes=IRIS_CLASS_NAMES,
        features=IRIS_FEATURE_NAMES,
        num_features=len(IRIS_FEATURE_NAMES),
        num_classes=len(IRIS_CLASS_NAMES),
    )


@app.post("/predict", response_model=PredictionResponse, summary="Predict Iris Class", tags=["Prediction"])
def predict(iris_input: IrisInput):
    """
    Accepts Iris flower measurements and returns the predicted class,
    class name, and confidence score.
    """
    if "model" not in app_state:
        raise HTTPException(status_code=503, detail="Model not loaded")

    model: LogisticRegression = app_state["model"]

    features = np.array([[
        iris_input.sepal_length,
        iris_input.sepal_width,
        iris_input.petal_length,
        iris_input.petal_width,
    ]])

    try:
        predicted_class = int(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0]
        confidence = float(round(probabilities[predicted_class], 4))
        class_name = IRIS_CLASS_NAMES[predicted_class]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(exc)}")

    return PredictionResponse(
        predicted_class=predicted_class,
        class_name=class_name,
        confidence=confidence,
    )
