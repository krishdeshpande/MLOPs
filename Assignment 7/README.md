# Assignment 7: Implement CI/CD Pipeline Using GitHub Actions

## Student Information

| Field | Details |
|-------|---------|
| **Name** | Krish Deshpande |
| **PRN** | 12414049 |
| **Roll No.** | 61 |
| **Class** | AIDS Div-C |

---

## Overview

This assignment demonstrates the implementation of a **CI/CD (Continuous Integration / Continuous Deployment) Pipeline** using **GitHub Actions** for a Machine Learning project.

## CI/CD Pipeline Overview

```
Push / Pull Request to main
           │
           ▼
    ┌──────────────┐
    │   CI: Test   │  ← Install deps, run pytest
    └──────┬───────┘
           │ (on main branch only)
           ▼
    ┌──────────────┐
    │  CD: Deploy  │  ← Echo deployment message
    └──────────────┘
```

### Pipeline Stages

1. **Trigger**: Activated on every `push` or `pull_request` to the `main` branch.
2. **Test Job** (`test`):
   - Runs on `ubuntu-latest` with Python 3.11
   - Installs dependencies from `requirements.txt`
   - Executes `pytest -v` to validate the ML model achieves ≥ 80% accuracy
3. **Deploy Job** (`deploy`):
   - Runs only after `test` succeeds
   - Triggered only when the branch is `main`
   - Simulates deployment of the trained ML model to production

## Project Structure

```
Assignment 6/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow definition
├── src/
│   └── model.py               # ML model training logic (Iris + LogisticRegression)
├── tests/
│   └── test_model.py          # Pytest tests for model accuracy
├── app.py                     # Main application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Model Details

- **Dataset**: Iris (from `sklearn.datasets`)
- **Algorithm**: Logistic Regression
- **Train/Test Split**: 80% / 20%
- **Accuracy Threshold**: ≥ 80%

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run the application
python app.py
```
