"""
Assignment 8 - Prometheus + Grafana Monitoring
Train and save the Iris classification model.

Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C
"""

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

def train_and_save_model(output_path: str = "model.pkl") -> float:
    """Train a Logistic Regression model on the Iris dataset and save it."""
    print("Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

    # Save model and class names together
    model_data = {
        "model": model,
        "target_names": iris.target_names.tolist(),
        "feature_names": iris.feature_names,
        "accuracy": accuracy,
    }
    joblib.dump(model_data, output_path)
    print(f"\nModel saved to: {os.path.abspath(output_path)}")
    return accuracy


if __name__ == "__main__":
    train_and_save_model("model.pkl")
