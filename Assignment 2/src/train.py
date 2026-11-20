"""
Assignment 2: MLflow Experiment Tracking
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C

This script trains multiple ML models on the Iris dataset, logs all
parameters, metrics, and artifacts to MLflow, and registers the best
model in the MLflow Model Registry.
"""

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
)

# ── Configuration ──────────────────────────────────────────────────────────────
EXPERIMENT_NAME = "Iris_Classification_Assignment2"
REGISTERED_MODEL_NAME = "BestIrisClassifier"
RANDOM_STATE = 42
TEST_SIZE = 0.2

# ── Data Preparation ───────────────────────────────────────────────────────────

def load_data():
    """Load and split the Iris dataset."""
    iris = load_iris(as_frame=True)
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    # Feature scaling (useful for Logistic Regression)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"Train size: {X_train.shape[0]} | Test size: {X_test.shape[0]}")
    return X_train_scaled, X_test_scaled, y_train, y_test, iris.target_names


def compute_metrics(y_true, y_pred):
    """Compute classification metrics."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred, average="weighted"),
        "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="weighted"),
    }


# ── MLflow Training ────────────────────────────────────────────────────────────

def train_and_log(model, model_name, params, X_train, X_test, y_train, y_test, target_names):
    """
    Train a single model and log everything to MLflow.
    Returns (run_id, accuracy) for later comparison.
    """
    with mlflow.start_run(run_name=model_name) as run:
        run_id = run.info.run_id
        print(f"\n[{model_name}] Run ID: {run_id}")

        # ── Log hyperparameters ───────────────────────────────────────────────
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("test_size", TEST_SIZE)
        mlflow.log_param("random_state", RANDOM_STATE)
        for key, value in params.items():
            mlflow.log_param(key, value)

        # ── Train ─────────────────────────────────────────────────────────────
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # ── Log metrics ───────────────────────────────────────────────────────
        metrics = compute_metrics(y_test, y_pred)
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)

        print(f"  Accuracy : {metrics['accuracy']:.4f}")
        print(f"  F1 Score : {metrics['f1_score']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall   : {metrics['recall']:.4f}")

        # ── Log classification report as artifact ────────────────────────────
        report = classification_report(y_test, y_pred, target_names=target_names)
        report_path = f"{model_name.replace(' ', '_')}_report.txt"
        with open(report_path, "w") as f:
            f.write(f"Model: {model_name}\n\n")
            f.write(report)
        mlflow.log_artifact(report_path)

        # ── Log model artifact ────────────────────────────────────────────────
        signature = infer_signature(X_train, y_pred)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            registered_model_name=None,  # Register separately for best model only
        )

        print(f"  Logged to MLflow ✓")
        return run_id, metrics["accuracy"]


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # Set (or create) the experiment
    mlflow.set_experiment(EXPERIMENT_NAME)
    print(f"MLflow Experiment: '{EXPERIMENT_NAME}'")
    print("=" * 60)

    # Load data
    X_train, X_test, y_train, y_test, target_names = load_data()

    # Define models and their hyperparameters
    models = [
        (
            "Logistic Regression",
            LogisticRegression(max_iter=200, random_state=RANDOM_STATE),
            {"max_iter": 200, "solver": "lbfgs", "multi_class": "auto"},
        ),
        (
            "Decision Tree",
            DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE),
            {"max_depth": 4, "criterion": "gini"},
        ),
        (
            "Random Forest",
            RandomForestClassifier(n_estimators=100, max_depth=5, random_state=RANDOM_STATE),
            {"n_estimators": 100, "max_depth": 5, "criterion": "gini"},
        ),
    ]

    # Train all models and collect results
    results = []
    for model_name, model, params in models:
        run_id, accuracy = train_and_log(
            model, model_name, params, X_train, X_test, y_train, y_test, target_names
        )
        results.append((model_name, run_id, accuracy, model))

    # ── Select and register best model ────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Summary of all runs:")
    results.sort(key=lambda x: x[2], reverse=True)
    for rank, (name, rid, acc, _) in enumerate(results, 1):
        print(f"  #{rank} {name:25s} | Accuracy: {acc:.4f} | Run: {rid}")

    best_name, best_run_id, best_acc, best_model = results[0]
    print(f"\nBest model: {best_name} (accuracy={best_acc:.4f})")

    # Register best model in Model Registry
    best_model_uri = f"runs:/{best_run_id}/model"
    registered = mlflow.register_model(
        model_uri=best_model_uri,
        name=REGISTERED_MODEL_NAME,
    )
    print(f"Registered '{REGISTERED_MODEL_NAME}' v{registered.version} in Model Registry ✓")
    print("\nOpen the MLflow UI:  mlflow ui  →  http://localhost:5000")


if __name__ == "__main__":
    main()
