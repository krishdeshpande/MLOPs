# Output Directory

This directory stores files generated when you run the pipeline.

## Generated Files

| File                    | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `transformed_data.csv`  | The feature-engineered dataset after the full pipeline has been applied.    |

## How to Generate

Run the main pipeline script from the project root:

```bash
python src/pipeline.py
```

The script will:
1. Load `data/dataset.csv`
2. Apply imputation, encoding, and scaling
3. Perform `SelectKBest` feature selection
4. Save the fitted pipeline to `models/feature_pipeline.pkl`
5. Write the transformed feature matrix to `output/transformed_data.csv`

> **Note:** The `models/` directory and `output/transformed_data.csv` are created automatically at runtime. They are excluded from version control via `.gitignore`.
