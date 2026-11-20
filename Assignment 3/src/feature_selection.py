"""
feature_selection.py
--------------------
Feature selection utilities using:
  - SelectKBest (with f_classif / chi2 scoring functions)
  - Pearson correlation analysis

Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C
"""

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif, chi2


# ---------------------------------------------------------------------------
# SelectKBest wrappers
# ---------------------------------------------------------------------------

def select_k_best_features(
    X: np.ndarray,
    y: np.ndarray,
    k: int = 5,
    score_func=f_classif,
    feature_names: list[str] | None = None,
) -> tuple[np.ndarray, list[str], np.ndarray]:
    """
    Select the top-*k* features using the specified scoring function.

    Parameters
    ----------
    X             : Feature matrix (n_samples, n_features).
    y             : Target vector (n_samples,).
    k             : Number of top features to keep.
    score_func    : Scoring function – f_classif (default) or chi2.
    feature_names : Optional list of column names for reporting.

    Returns
    -------
    X_selected    : Reduced feature matrix (n_samples, k).
    selected_names: Names of the selected features (or index strings if names
                    were not provided).
    scores        : Full score array for every input feature.
    """
    selector = SelectKBest(score_func=score_func, k=k)
    X_selected = selector.fit_transform(X, y)

    scores = selector.scores_
    support = selector.get_support()

    if feature_names is not None:
        all_names = np.array(feature_names)
        selected_names = all_names[support].tolist()
    else:
        selected_names = [f"feature_{i}" for i, s in enumerate(support) if s]

    return X_selected, selected_names, scores


def feature_score_report(
    scores: np.ndarray,
    feature_names: list[str] | None = None,
    top_k: int = 10,
) -> pd.DataFrame:
    """
    Return a sorted DataFrame of feature scores.

    Parameters
    ----------
    scores        : Score array returned by SelectKBest.scores_.
    feature_names : Column names corresponding to scores.
    top_k         : How many top features to include in the report.

    Returns
    -------
    DataFrame with columns ['Feature', 'Score'] sorted descending.
    """
    names = feature_names if feature_names is not None else [f"feature_{i}" for i in range(len(scores))]
    report = pd.DataFrame({"Feature": names, "Score": scores})
    report = report.sort_values("Score", ascending=False).head(top_k).reset_index(drop=True)
    return report


# ---------------------------------------------------------------------------
# Correlation analysis
# ---------------------------------------------------------------------------

def correlation_with_target(
    df: pd.DataFrame,
    target_col: str,
    method: str = "pearson",
) -> pd.Series:
    """
    Compute the absolute correlation of each numerical feature with the target.

    Parameters
    ----------
    df         : DataFrame containing features and the target column.
    target_col : Name of the target column.
    method     : 'pearson' | 'spearman' | 'kendall'

    Returns
    -------
    Series of absolute correlations, sorted descending.
    """
    numerics = df.select_dtypes(include=[np.number]).drop(columns=[target_col], errors="ignore")
    corr = numerics.corrwith(df[target_col], method=method).abs()
    return corr.sort_values(ascending=False)


def correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """
    Return the correlation matrix for all numerical columns in *df*.
    """
    numerics = df.select_dtypes(include=[np.number])
    return numerics.corr(method=method)


def drop_highly_correlated(df: pd.DataFrame, threshold: float = 0.90) -> pd.DataFrame:
    """
    Remove features that are correlated above *threshold* with another feature
    to reduce multicollinearity.

    Parameters
    ----------
    df        : Feature DataFrame (no target column).
    threshold : Correlation coefficient above which one of a pair is dropped.

    Returns
    -------
    Reduced DataFrame.
    """
    corr_matrix = df.corr().abs()
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper_tri.columns if any(upper_tri[col] > threshold)]
    print(f"[drop_highly_correlated] Dropping {len(to_drop)} column(s): {to_drop}")
    return df.drop(columns=to_drop)


# ---------------------------------------------------------------------------
# Quick demo (run as script)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from sklearn.datasets import load_iris

    iris = load_iris(as_frame=True)
    X_df = iris.frame.drop(columns=["target"])
    y = iris.target

    print("=== Correlation with target ===")
    df_full = iris.frame.rename(columns={"target": "Survived"})
    print(correlation_with_target(df_full, target_col="Survived"))

    print("\n=== SelectKBest (f_classif, k=2) ===")
    X_sel, names, scores = select_k_best_features(
        X_df.values, y.values, k=2, feature_names=list(X_df.columns)
    )
    print("Selected features:", names)
    print(feature_score_report(scores, feature_names=list(X_df.columns)))
