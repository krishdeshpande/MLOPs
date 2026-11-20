"""
Assignment 2: MLflow Experiment Tracking
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C

This script compares all MLflow experiment runs programmatically using
mlflow.search_runs(), prints a ranked summary, and highlights the best model.
"""

import mlflow
import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────
EXPERIMENT_NAME = "Iris_Classification_Assignment2"
REGISTERED_MODEL_NAME = "BestIrisClassifier"

# Columns to display in the comparison table
DISPLAY_COLS = [
    "tags.mlflow.runName",
    "params.model_name",
    "params.max_iter",
    "params.max_depth",
    "params.n_estimators",
    "metrics.accuracy",
    "metrics.f1_score",
    "metrics.precision",
    "metrics.recall",
    "info.run_id",
    "info.status",
]


def compare_experiments():
    """Search all runs in the experiment and display a comparison table."""

    # ── Fetch experiment ───────────────────────────────────────────────────────
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        print(f"[ERROR] Experiment '{EXPERIMENT_NAME}' not found.")
        print("Please run src/train.py first to generate experiment data.")
        return

    experiment_id = experiment.experiment_id
    print(f"Experiment : {EXPERIMENT_NAME}")
    print(f"Experiment ID: {experiment_id}")
    print("=" * 70)

    # ── Search all runs ────────────────────────────────────────────────────────
    runs_df = mlflow.search_runs(
        experiment_ids=[experiment_id],
        order_by=["metrics.accuracy DESC"],
    )

    if runs_df.empty:
        print("No runs found. Run src/train.py first.")
        return

    print(f"Total runs found: {len(runs_df)}\n")

    # ── Build comparison table ─────────────────────────────────────────────────
    # Keep only columns that actually exist in the dataframe
    available_cols = [c for c in DISPLAY_COLS if c in runs_df.columns]
    comparison = runs_df[available_cols].copy()

    # Rename for readability
    rename_map = {
        "tags.mlflow.runName": "Run Name",
        "params.model_name": "Model",
        "params.max_iter": "max_iter",
        "params.max_depth": "max_depth",
        "params.n_estimators": "n_estimators",
        "metrics.accuracy": "Accuracy",
        "metrics.f1_score": "F1 Score",
        "metrics.precision": "Precision",
        "metrics.recall": "Recall",
        "info.run_id": "Run ID",
        "info.status": "Status",
    }
    comparison.rename(columns=rename_map, inplace=True)

    # Reset index for clean display
    comparison.reset_index(drop=True, inplace=True)
    comparison.index += 1  # 1-based ranking

    # Round numeric columns
    for col in ["Accuracy", "F1 Score", "Precision", "Recall"]:
        if col in comparison.columns:
            comparison[col] = comparison[col].apply(
                lambda x: f"{float(x):.4f}" if pd.notna(x) else "N/A"
            )

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 120)
    pd.set_option("display.max_colwidth", 30)

    print("── Experiment Run Comparison (sorted by Accuracy ↓) ──")
    print(comparison.to_string())

    # ── Best run summary ───────────────────────────────────────────────────────
    best = runs_df.iloc[0]
    print("\n" + "=" * 70)
    print("BEST RUN")
    print("=" * 70)
    print(f"  Run Name  : {best.get('tags.mlflow.runName', 'N/A')}")
    print(f"  Run ID    : {best['run_id']}")
    print(f"  Accuracy  : {best.get('metrics.accuracy', 'N/A'):.4f}")
    print(f"  F1 Score  : {best.get('metrics.f1_score', 'N/A'):.4f}")
    print(f"  Precision : {best.get('metrics.precision', 'N/A'):.4f}")
    print(f"  Recall    : {best.get('metrics.recall', 'N/A'):.4f}")

    # ── Registered Model info ──────────────────────────────────────────────────
    print("\n── Registered Model Info ──")
    try:
        client = mlflow.tracking.MlflowClient()
        versions = client.search_model_versions(f"name='{REGISTERED_MODEL_NAME}'")
        if versions:
            latest = sorted(versions, key=lambda v: int(v.version), reverse=True)[0]
            print(f"  Model Name : {latest.name}")
            print(f"  Version    : {latest.version}")
            print(f"  Stage      : {latest.current_stage}")
            print(f"  Source Run : {latest.run_id}")
        else:
            print(f"  No versions found for '{REGISTERED_MODEL_NAME}'.")
    except Exception as e:
        print(f"  Could not retrieve model registry info: {e}")

    print("\nTip: Run `mlflow ui` and open http://localhost:5000 for the full UI.")


if __name__ == "__main__":
    compare_experiments()
