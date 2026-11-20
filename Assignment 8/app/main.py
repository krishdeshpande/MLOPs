"""
Assignment 8 - Prometheus + Grafana Monitoring
FastAPI ML Inference API with Prometheus instrumentation.

Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C
"""

import time
import os
import joblib
import numpy as np
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    multiprocess,
    REGISTRY,
)

# ---------------------------------------------------------------------------
# Prometheus Metrics
# ---------------------------------------------------------------------------
PREDICTION_REQUESTS_TOTAL = Counter(
    "prediction_requests_total",
    "Total number of prediction requests",
    ["status"],          # label: 'success' or 'error'
)

PREDICTION_LATENCY_SECONDS = Histogram(
    "prediction_latency_seconds",
    "Time spent processing a prediction request",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

# ---------------------------------------------------------------------------
# Global Model State
# ---------------------------------------------------------------------------
model_data: dict = {}


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML model at startup."""
    model_path = os.getenv("MODEL_PATH", "model.pkl")
    if not os.path.exists(model_path):
        # Train and save if not found (useful for first run inside Docker)
        print(f"Model file '{model_path}' not found. Training now...")
        from train_model import train_and_save_model
        train_and_save_model(model_path)

    print(f"Loading model from '{model_path}'...")
    global model_data
    model_data = joblib.load(model_path)
    print(f"Model loaded. Classes: {model_data['target_names']}")
    yield
    # Shutdown
    model_data.clear()
    print("Model unloaded.")


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Iris ML API with Prometheus Monitoring",
    description=(
        "Assignment 8 — Prometheus + Grafana monitoring for a FastAPI ML service. "
        "Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | AIDS Div-C"
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class IrisInput(BaseModel):
    sepal_length: float = Field(..., gt=0, example=5.1, description="Sepal length in cm")
    sepal_width:  float = Field(..., gt=0, example=3.5, description="Sepal width in cm")
    petal_length: float = Field(..., gt=0, example=1.4, description="Petal length in cm")
    petal_width:  float = Field(..., gt=0, example=0.2, description="Petal width in cm")


class PredictionResponse(BaseModel):
    predicted_class: int
    class_name: str
    confidence: float
    input_features: list[float]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["General"])
def root():
    """Welcome endpoint."""
    return {
        "message": "Iris ML API with Prometheus Monitoring",
        "assignment": "Assignment 8 — MLOps",
        "student": "Krish Deshpande | PRN: 12414049 | Roll: 61 | AIDS Div-C",
        "endpoints": {
            "predict": "POST /predict",
            "metrics": "GET /metrics",
            "health":  "GET /health",
            "docs":    "GET /docs",
        },
    }


@app.get("/health", tags=["General"])
def health_check():
    """Health check endpoint."""
    model_loaded = bool(model_data.get("model"))
    return {
        "status": "ok" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "model_accuracy": model_data.get("accuracy"),
    }


@app.post("/predict", response_model=PredictionResponse, tags=["ML"])
def predict(payload: IrisInput):
    """
    Perform an Iris species prediction.

    Records:
    - `prediction_requests_total` counter (labels: status=success/error)
    - `prediction_latency_seconds` histogram
    """
    if not model_data.get("model"):
        PREDICTION_REQUESTS_TOTAL.labels(status="error").inc()
        raise HTTPException(status_code=503, detail="Model not loaded")

    start_time = time.time()
    try:
        features = np.array([[
            payload.sepal_length,
            payload.sepal_width,
            payload.petal_length,
            payload.petal_width,
        ]])

        model = model_data["model"]
        predicted_class = int(model.predict(features)[0])
        probabilities   = model.predict_proba(features)[0]
        confidence      = float(probabilities[predicted_class])
        class_name      = model_data["target_names"][predicted_class]

        # Record success metric
        PREDICTION_REQUESTS_TOTAL.labels(status="success").inc()

        return PredictionResponse(
            predicted_class=predicted_class,
            class_name=class_name,
            confidence=round(confidence, 4),
            input_features=features[0].tolist(),
        )

    except Exception as exc:
        PREDICTION_REQUESTS_TOTAL.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(exc)}")

    finally:
        elapsed = time.time() - start_time
        PREDICTION_LATENCY_SECONDS.observe(elapsed)


@app.get("/metrics", tags=["Monitoring"])
def metrics():
    """Expose Prometheus metrics in text format (scraped by Prometheus)."""
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST,
    )


# ---------------------------------------------------------------------------
# Entry point (for local development)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
