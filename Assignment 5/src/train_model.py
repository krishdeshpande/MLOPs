"""
Assignment 5: REST API using FastAPI
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C

Script to train an Iris classifier (Logistic Regression) and save as model.pkl
"""

import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os


def train_and_save_model(output_path: str = "model.pkl") -> None:
    """Train a Logistic Regression model on the Iris dataset and save it."""

    # Load dataset
    iris = load_iris()
    X, y = iris.data, iris.target

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train model
    model = LogisticRegression(max_iter=200, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

    # Resolve output path relative to project root (parent of src/)
    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(src_dir)
    full_output_path = os.path.join(project_root, output_path)

    # Save model
    joblib.dump(model, full_output_path)
    print(f"Model saved to: {full_output_path}")


if __name__ == "__main__":
    train_and_save_model()
