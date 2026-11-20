"""
Flask app to serve Iris classification predictions.
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C
"""

from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load model at startup
MODEL_PATH = "model.joblib"
CLASS_NAMES = ["setosa", "versicolor", "virginica"]

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    raise RuntimeError(
        f"Model file '{MODEL_PATH}' not found. Run train_model.py first."
    )


@app.route("/", methods=["GET"])
def home():
    """Welcome endpoint."""
    return jsonify({
        "message": "Welcome to the Iris Classification API!",
        "student": {
            "name": "Krish Deshpande",
            "PRN": "12414049",
            "roll": 61,
            "class": "AIDS Div-C"
        },
        "usage": {
            "predict": "POST /predict with JSON body {'features': [5.1, 3.5, 1.4, 0.2]}"
        }
    })


@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts JSON: {"features": [sepal_length, sepal_width, petal_length, petal_width]}
    Returns:      {"prediction": 0, "class_name": "setosa"}
    """
    data = request.get_json(force=True)

    if data is None or "features" not in data:
        return jsonify({"error": "Request body must be JSON with a 'features' key"}), 400

    features = data["features"]

    if not isinstance(features, list) or len(features) != 4:
        return jsonify({"error": "'features' must be a list of exactly 4 numeric values"}), 400

    try:
        features_array = np.array(features, dtype=float).reshape(1, -1)
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid feature values: {str(e)}"}), 400

    prediction = int(model.predict(features_array)[0])
    class_name = CLASS_NAMES[prediction]

    return jsonify({
        "prediction": prediction,
        "class_name": class_name
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
