"""
Assignment 4 – Apache Airflow DAG: Data Pipeline
-------------------------------------------------
Student  : Krish Deshpande
PRN      : 12414049
Roll No. : 61
Class    : AIDS Div-C

DAG ID   : data_pipeline_dag
Schedule : @daily  (catchup disabled)
Operator : PythonOperator

Task chain: extract >> validate >> process >> report >> notify
"""

from datetime import datetime
import os

import numpy as np
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

# ---------------------------------------------------------------------------
# File paths used across tasks
# ---------------------------------------------------------------------------
EXTRACTED_PATH = "/tmp/extracted_data.csv"
PROCESSED_PATH = "/tmp/processed_data.csv"
REPORT_PATH    = "/tmp/report.txt"


# ---------------------------------------------------------------------------
# Task 1 – Extract
# ---------------------------------------------------------------------------
def extract():
    """Generate sample CSV data and save to /tmp/extracted_data.csv."""
    print("=== [Task 1] EXTRACT: Generating sample dataset ===")

    np.random.seed(42)
    n_rows = 200

    data = {
        "id":         range(1, n_rows + 1),
        "name":       [f"Record_{i}" for i in range(1, n_rows + 1)],
        "age":        np.where(
                          np.random.rand(n_rows) < 0.08,   # ~8 % missing
                          np.nan,
                          np.random.randint(18, 65, n_rows).astype(float),
                      ),
        "salary":     np.where(
                          np.random.rand(n_rows) < 0.05,   # ~5 % missing
                          np.nan,
                          np.round(np.random.uniform(30_000, 120_000, n_rows), 2),
                      ),
        "department": np.where(
                          np.random.rand(n_rows) < 0.04,   # ~4 % missing
                          None,
                          np.random.choice(
                              ["Engineering", "Marketing", "Sales",
                               "HR", "Finance"],
                              n_rows,
                          ),
                      ),
        "score":      np.where(
                          np.random.rand(n_rows) < 0.06,   # ~6 % missing
                          np.nan,
                          np.round(np.random.uniform(0, 100, n_rows), 1),
                      ),
        "join_date":  pd.date_range(start="2020-01-01", periods=n_rows, freq="D"),
    }

    df = pd.DataFrame(data)
    df.to_csv(EXTRACTED_PATH, index=False)

    print(f"  Rows generated : {len(df)}")
    print(f"  Columns        : {list(df.columns)}")
    print(f"  Saved to       : {EXTRACTED_PATH}")
    print("=== [Task 1] EXTRACT: Complete ===\n")


# ---------------------------------------------------------------------------
# Task 2 – Validate
# ---------------------------------------------------------------------------
def validate():
    """Read extracted CSV, check for missing values, print validation stats."""
    print("=== [Task 2] VALIDATE: Running data quality checks ===")

    if not os.path.exists(EXTRACTED_PATH):
        raise FileNotFoundError(
            f"Extracted data not found at {EXTRACTED_PATH}. "
            "Ensure the 'extract' task ran successfully."
        )

    df = pd.read_csv(EXTRACTED_PATH)

    total_rows   = len(df)
    total_cols   = len(df.columns)
    missing_per_col = df.isnull().sum()
    total_missing   = int(missing_per_col.sum())

    print(f"\n  Total rows    : {total_rows}")
    print(f"  Total columns : {total_cols}")
    print(f"  Total missing : {total_missing}")
    print("\n  Missing values per column:")
    for col, cnt in missing_per_col.items():
        pct = cnt / total_rows * 100
        status = "⚠ MISSING" if cnt > 0 else "✓ OK"
        print(f"    {col:<12} : {cnt:>3}  ({pct:5.1f} %)  {status}")

    # Simple rule: fail if any column has > 20 % missing
    critical_cols = [
        col for col, cnt in missing_per_col.items()
        if cnt / total_rows > 0.20
    ]
    if critical_cols:
        raise ValueError(
            f"Validation FAILED – columns exceed 20 % missing: {critical_cols}"
        )

    print("\n  Validation PASSED – data quality is acceptable.")
    print("=== [Task 2] VALIDATE: Complete ===\n")


# ---------------------------------------------------------------------------
# Task 3 – Process
# ---------------------------------------------------------------------------
def process():
    """Clean and transform the data, save processed CSV."""
    print("=== [Task 3] PROCESS: Cleaning and transforming data ===")

    df = pd.read_csv(EXTRACTED_PATH)
    original_rows = len(df)

    # --- Impute missing numerics with column median ---
    for col in ["age", "salary", "score"]:
        median_val = df[col].median()
        missing_cnt = df[col].isnull().sum()
        df[col].fillna(median_val, inplace=True)
        if missing_cnt:
            print(f"  Imputed {missing_cnt} missing '{col}' values with median ({median_val:.2f})")

    # --- Fill missing department with 'Unknown' ---
    missing_dept = df["department"].isnull().sum()
    df["department"].fillna("Unknown", inplace=True)
    if missing_dept:
        print(f"  Filled {missing_dept} missing 'department' values with 'Unknown'")

    # --- Type casts ---
    df["age"]  = df["age"].astype(int)
    df["id"]   = df["id"].astype(int)

    # --- Derived features ---
    df["salary_band"] = pd.cut(
        df["salary"],
        bins=[0, 50_000, 80_000, float("inf")],
        labels=["Low", "Medium", "High"],
    )
    df["score_grade"] = df["score"].apply(
        lambda s: "A" if s >= 80 else ("B" if s >= 60 else ("C" if s >= 40 else "D"))
    )
    df["join_date"] = pd.to_datetime(df["join_date"])
    df["join_year"]  = df["join_date"].dt.year
    df["join_month"] = df["join_date"].dt.month

    # --- Save ---
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"\n  Rows before : {original_rows}")
    print(f"  Rows after  : {len(df)}")
    print(f"  Columns     : {list(df.columns)}")
    print(f"  Saved to    : {PROCESSED_PATH}")
    print("=== [Task 3] PROCESS: Complete ===\n")


# ---------------------------------------------------------------------------
# Task 4 – Report
# ---------------------------------------------------------------------------
def report():
    """Generate a summary report and save to /tmp/report.txt."""
    print("=== [Task 4] REPORT: Generating summary report ===")

    df = pd.read_csv(PROCESSED_PATH)

    record_count   = len(df)
    missing_values = int(df.isnull().sum().sum())   # should be 0 after processing

    dept_counts    = df["department"].value_counts().to_dict()
    band_counts    = df["salary_band"].value_counts().to_dict()
    grade_counts   = df["score_grade"].value_counts().sort_index().to_dict()
    avg_salary     = df["salary"].mean()
    avg_score      = df["score"].mean()
    avg_age        = df["age"].mean()

    report_lines = [
        "=" * 60,
        "         DATA PIPELINE – SUMMARY REPORT",
        "=" * 60,
        f"  Generated At     : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        f"  Pipeline         : data_pipeline_dag",
        "",
        "--- Dataset Statistics ---",
        f"  Total Records    : {record_count}",
        f"  Missing Values   : {missing_values}",
        f"  Avg Age          : {avg_age:.1f} years",
        f"  Avg Salary       : ${avg_salary:,.2f}",
        f"  Avg Score        : {avg_score:.1f}",
        "",
        "--- Department Breakdown ---",
    ]
    for dept, cnt in sorted(dept_counts.items()):
        report_lines.append(f"    {dept:<15}: {cnt}")

    report_lines += [
        "",
        "--- Salary Bands ---",
    ]
    for band, cnt in sorted(band_counts.items()):
        report_lines.append(f"    {band:<10}: {cnt}")

    report_lines += [
        "",
        "--- Score Grades ---",
    ]
    for grade, cnt in sorted(grade_counts.items()):
        report_lines.append(f"    Grade {grade}: {cnt}")

    report_lines += [
        "",
        "--- Pipeline Status ---",
        "  Status           : SUCCESS",
        "  All tasks        : extract > validate > process > report > notify",
        "=" * 60,
    ]

    report_text = "\n".join(report_lines)
    with open(REPORT_PATH, "w") as f:
        f.write(report_text)

    print(report_text)
    print(f"\n  Report saved to : {REPORT_PATH}")
    print("=== [Task 4] REPORT: Complete ===\n")


# ---------------------------------------------------------------------------
# Task 5 – Notify
# ---------------------------------------------------------------------------
def notify():
    """Print a success notification confirming the pipeline completed."""
    print("=== [Task 5] NOTIFY: Pipeline Completion Notification ===")
    print()
    print("  ✅  DATA PIPELINE COMPLETED SUCCESSFULLY!")
    print()
    print("  Summary:")
    print(f"    DAG          : data_pipeline_dag")
    print(f"    Completed At : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"    Tasks run    : extract → validate → process → report → notify")
    print(f"    Output files :")
    print(f"      • {EXTRACTED_PATH}")
    print(f"      • {PROCESSED_PATH}")
    print(f"      • {REPORT_PATH}")
    print()
    print("  All downstream systems can now consume the processed data.")
    print("=== [Task 5] NOTIFY: Complete ===\n")


# ---------------------------------------------------------------------------
# DAG Definition
# ---------------------------------------------------------------------------
default_args = {
    "owner":           "Krish Deshpande",
    "retries":         1,
    "email_on_failure": False,
    "email_on_retry":   False,
}

with DAG(
    dag_id="data_pipeline_dag",
    default_args=default_args,
    description="Assignment 4 – ETL data pipeline with validation and reporting",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["mlops", "assignment4", "aids"],
) as dag:

    t1 = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    t2 = PythonOperator(
        task_id="validate",
        python_callable=validate,
    )

    t3 = PythonOperator(
        task_id="process",
        python_callable=process,
    )

    t4 = PythonOperator(
        task_id="report",
        python_callable=report,
    )

    t5 = PythonOperator(
        task_id="notify",
        python_callable=notify,
    )

    # Task dependency chain
    t1 >> t2 >> t3 >> t4 >> t5
