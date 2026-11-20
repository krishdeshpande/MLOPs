"""
preprocessing.py
----------------
Standalone helper functions for common preprocessing steps:
  - Handling missing values
  - Encoding categorical features
  - Scaling numerical features

These utilities are thin wrappers around scikit-learn transformers and can be
used independently of the full Pipeline defined in pipeline.py.

Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# ---------------------------------------------------------------------------
# Missing-value handling
# ---------------------------------------------------------------------------

def impute_numerical(df: pd.DataFrame, columns: list[str], strategy: str = "mean") -> pd.DataFrame:
    """
    Fill missing values in numerical columns using the specified strategy.

    Parameters
    ----------
    df       : Input DataFrame (not modified in place).
    columns  : List of numerical column names to impute.
    strategy : 'mean' | 'median' | 'most_frequent' | 'constant'

    Returns
    -------
    DataFrame with missing values in *columns* filled.
    """
    df = df.copy()
    imputer = SimpleImputer(strategy=strategy)
    df[columns] = imputer.fit_transform(df[columns])
    return df


def impute_categorical(df: pd.DataFrame, columns: list[str], fill_value: str = "Unknown") -> pd.DataFrame:
    """
    Fill missing values in categorical columns with *fill_value* (constant strategy).

    Parameters
    ----------
    df         : Input DataFrame (not modified in place).
    columns    : List of categorical column names to impute.
    fill_value : The constant used to fill NaNs.

    Returns
    -------
    DataFrame with missing categorical values filled.
    """
    df = df.copy()
    imputer = SimpleImputer(strategy="constant", fill_value=fill_value)
    df[columns] = imputer.fit_transform(df[columns])
    return df


def report_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary DataFrame of missing-value counts and percentages.
    """
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    summary = pd.DataFrame({"Missing Count": missing, "Missing %": pct})
    return summary[summary["Missing Count"] > 0].sort_values("Missing Count", ascending=False)


# ---------------------------------------------------------------------------
# Categorical encoding
# ---------------------------------------------------------------------------

def one_hot_encode(df: pd.DataFrame, columns: list[str], drop: str = "first") -> pd.DataFrame:
    """
    Apply one-hot encoding to the specified columns and return the updated
    DataFrame (original columns are dropped and replaced by binary dummies).

    Parameters
    ----------
    df      : Input DataFrame (not modified in place).
    columns : Categorical columns to encode.
    drop    : Passed to pd.get_dummies as *drop_first* equivalent.
              Use 'first' to avoid multicollinearity; None to keep all.

    Returns
    -------
    DataFrame with one-hot-encoded columns.
    """
    df = df.copy()
    drop_first = drop == "first"
    dummies = pd.get_dummies(df[columns], drop_first=drop_first, dtype=int)
    df = df.drop(columns=columns)
    df = pd.concat([df, dummies], axis=1)
    return df


def sklearn_one_hot_encode(X: np.ndarray, sparse_output: bool = False) -> np.ndarray:
    """
    Thin wrapper around sklearn's OneHotEncoder.
    Expects *X* to be a 2-D array of categorical values.

    Returns
    -------
    Dense numpy array of one-hot-encoded features.
    """
    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=sparse_output)
    return enc.fit_transform(X)


# ---------------------------------------------------------------------------
# Numerical scaling
# ---------------------------------------------------------------------------

def standard_scale(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Apply StandardScaler (zero mean, unit variance) to numerical columns.

    Parameters
    ----------
    df      : Input DataFrame (not modified in place).
    columns : Numerical columns to scale.

    Returns
    -------
    DataFrame with scaled values in *columns*.
    """
    df = df.copy()
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def describe_numerical(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Return descriptive statistics for the given numerical columns.
    """
    return df[columns].describe().T
