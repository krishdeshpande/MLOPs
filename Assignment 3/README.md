# Assignment 3: Feature Engineering Pipeline

## Student Information
| Field  | Details           |
|--------|-------------------|
| Name   | Krish Deshpande   |
| PRN    | 12414049          |
| Roll   | 61                |
| Class  | AIDS Div-C        |

---

## Objective

Build an end-to-end **Feature Engineering Pipeline** using `scikit-learn` on a Titanic-like dataset. The pipeline covers:

- Handling missing values via `SimpleImputer`
- Encoding categorical features with `OneHotEncoder`
- Scaling numerical features using `StandardScaler`
- Selecting the most informative features with `SelectKBest` (chi2 / f_classif)
- Wrapping everything in a reusable `sklearn.pipeline.Pipeline` + `ColumnTransformer`
- Persisting the fitted pipeline to disk with `joblib`

---

## Project Structure

```
Assignment 3/
├── data/
│   └── dataset.csv           # Titanic-like raw dataset
├── models/
│   └── feature_pipeline.pkl  # Saved pipeline (generated on run)
├── output/
│   └── README.md             # Notes on generated output
├── src/
│   ├── preprocessing.py      # Standalone preprocessing helpers
│   ├── feature_selection.py  # SelectKBest + correlation analysis
│   └── pipeline.py           # Main script – builds, runs, saves pipeline
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
pip install -r requirements.txt
python src/pipeline.py
```

The script will print:
- Original dataset shape
- Transformed feature shape after the pipeline
- Names of selected features

The fitted pipeline is saved to `models/feature_pipeline.pkl`.
