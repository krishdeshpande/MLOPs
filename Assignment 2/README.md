# Assignment 2: MLflow Experiment Tracking

## Student Information
| Field | Details |
|-------|---------|
| **Name** | Krish Deshpande |
| **PRN** | 12414049 |
| **Roll No.** | 61 |
| **Class** | AIDS Div-C |

## Objective
The objective of this assignment is to understand and implement **MLflow Experiment Tracking** for machine learning workflows. This includes:

- Setting up MLflow tracking for multiple machine learning experiments
- Training multiple classification models on the Iris dataset (Logistic Regression, Decision Tree, Random Forest)
- Logging hyperparameters, evaluation metrics, and model artifacts to MLflow
- Comparing experiment runs using the MLflow UI and programmatic APIs
- Registering the best-performing model in the **MLflow Model Registry**

## Project Structure
```
Assignment 2/
├── README.md
├── requirements.txt
└── src/
    ├── train.py                 # Train models and log experiments to MLflow
    └── compare_experiments.py  # Compare and analyze MLflow experiment runs
```

## Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MLflow Tracking Server (optional, uses local by default)
```bash
mlflow ui
```

### 3. Run Training Script
```bash
python src/train.py
```

### 4. Compare Experiments
```bash
python src/compare_experiments.py
```

### 5. View Results
Open your browser and navigate to: [http://localhost:5000](http://localhost:5000)

## Key MLflow Concepts Covered
- `mlflow.start_run()` — Start a new MLflow run context
- `mlflow.log_param()` — Log hyperparameters
- `mlflow.log_metric()` — Log evaluation metrics (accuracy, F1-score, etc.)
- `mlflow.sklearn.log_model()` — Log trained sklearn model artifacts
- `mlflow.search_runs()` — Programmatically search and compare runs
- **MLflow Model Registry** — Register and version the best model
