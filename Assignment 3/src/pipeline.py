"""
Assignment 3: Feature Engineering Pipeline
Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | AIDS Div-C
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset.csv')
MODEL_DIR   = os.path.join(os.path.dirname(__file__), '..', 'models')
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(MODEL_DIR,  exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Step 1: Load Dataset ───────────────────────────────────────────────────────
print("Step 1: Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"Dataset Loaded Successfully")
print(f"Original Dataset Shape: {df.shape}")
print(df.head())

# ── Step 2: Data Cleaning ──────────────────────────────────────────────────────
print("\nStep 2: Data Cleaning...")
df.drop_duplicates(inplace=True)
print(f"Missing Values Before Cleaning:\n{df.isnull().sum()}")

# ── Step 3 & 5: Feature Engineering + Pipeline ────────────────────────────────
print("\nStep 3: Building Feature Engineering Pipeline...")

TARGET      = 'Survived'
NUMERIC     = ['Age', 'Fare']
CATEGORICAL = ['Sex', 'Embarked', 'Pclass']

X = df[NUMERIC + CATEGORICAL]
y = df[TARGET]

numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler()),
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline,  NUMERIC),
    ('cat', categorical_pipeline, CATEGORICAL),
])

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('selector',     SelectKBest(score_func=f_classif, k=4)),
])

# ── Step 6: Transform Dataset ──────────────────────────────────────────────────
print("\nStep 6: Transforming dataset...")
X_transformed = full_pipeline.fit_transform(X, y)
print(f"Numerical Features Scaled")
print(f"Categorical Features Encoded")
print(f"Missing Values Removed")
print(f"Original Dataset Shape: {X.shape}")
print(f"Transformed Dataset Shape: {X_transformed.shape}")

# Save transformed data
transformed_df = pd.DataFrame(X_transformed)
transformed_df.to_csv(os.path.join(OUTPUT_DIR, 'transformed_data.csv'), index=False)
print(f"Transformed data saved to output/transformed_data.csv")

# ── Step 7: Save Pipeline ──────────────────────────────────────────────────────
print("\nStep 7: Saving pipeline...")
pipeline_path = os.path.join(MODEL_DIR, 'feature_pipeline.pkl')
joblib.dump(full_pipeline, pipeline_path)
print(f"Pipeline Saved Successfully → models/feature_pipeline.pkl")

# ── Step 8: Reuse Pipeline ─────────────────────────────────────────────────────
print("\nStep 8: Reusing saved pipeline on new sample data...")
loaded_pipeline = joblib.load(pipeline_path)
sample = pd.DataFrame([{
    'Age': 28.0, 'Fare': 15.5, 'SibSp': 0, 'Parch': 0,
    'Sex': 'male', 'Embarked': 'S', 'Pclass': 3
}])
sample_transformed = loaded_pipeline.transform(sample)
print(f"Sample transformed shape: {sample_transformed.shape}")
print("Pipeline reuse successful!")
