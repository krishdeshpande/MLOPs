import sys
import os

# Allow importing from the src directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.model import train_model


def test_model_accuracy():
    """
    Test that the trained Logistic Regression model achieves
    at least 80% accuracy on the Iris test set.
    """
    accuracy = train_model()
    assert accuracy >= 0.80, (
        f"Model accuracy {accuracy:.4f} is below the required threshold of 0.80"
    )


def test_model_returns_float():
    """
    Test that train_model() returns a float value.
    """
    accuracy = train_model()
    assert isinstance(accuracy, float), (
        f"Expected train_model() to return a float, got {type(accuracy)}"
    )


def test_model_accuracy_in_range():
    """
    Test that the accuracy is a valid probability (between 0 and 1).
    """
    accuracy = train_model()
    assert 0.0 <= accuracy <= 1.0, (
        f"Accuracy {accuracy} is out of valid range [0, 1]"
    )
