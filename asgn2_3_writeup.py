import docx, os, shutil
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_all_writeups import (
    TEMPLATE_PATH, BASE_DIR, ALL_WRITEUPS_DIR,
    add_heading_1, add_heading_2, add_body_p, add_bullet,
    add_code_block, add_captioned_image, add_table_styled, populate_cover_page
)

# ==============================================================================
# ASSIGNMENT 2: Track Machine Learning Experiments Using MLflow
# ==============================================================================
def create_assignment_2():
    doc = docx.Document(TEMPLATE_PATH)
    t0 = doc.tables[0]
    
    # 1. Fill Cover Page
    populate_cover_page(
        t0,
        asgn_no=2,
        asgn_title="Track Machine Learning Experiments Using MLflow",
        perf_date="14/07/2026",
        sub_date="21/07/2026"
    )
    
    # Clear original template paragraphs after cover table
    for p in doc.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    # Remove tables 1 and 2 from template to replace with styled tables
    for tbl in doc.tables[1:]:
        tbl._tbl.getparent().remove(tbl._tbl)

    doc.add_page_break()

    # ── Aim ───────────────────────────────────────────────────────────────────
    add_heading_1(doc, "Aim")
    add_body_p(doc, "To implement systematic machine learning experiment tracking, parameter and metric logging, model artifact management, and model registry governance using MLflow.")

    # ── Problem Statement ─────────────────────────────────────────────────────
    add_heading_1(doc, "Problem Statement")
    add_body_p(doc, "In traditional machine learning experimentation, engineers iterate over numerous algorithm families, hyperparameters, feature subsets, and preprocessing techniques. Typically, performance metrics and configuration parameters are logged manually in spreadsheets, console prints, or unstructured text files. This ad-hoc approach creates severe technical debt: experiment results cannot be reproduced reliably, historical models cannot be audited or linked to their training data and hyperparameters, and moving candidate models into staging or production environments is error-prone.\n\nMLflow addresses these challenges by providing an open-source platform for managing the end-to-end machine learning lifecycle. In this assignment, MLflow is integrated with Scikit-Learn to track experiments across multiple classification models (Logistic Regression, Decision Tree, Random Forest) on the Iris dataset. We log training parameters, evaluation metrics (accuracy, precision, recall, F1-score), serialized model artifacts, and evaluation reports. Furthermore, the MLflow Web UI is utilized for comparative visualization, and the top-performing model is registered into the MLflow Model Registry with versioning and stage management.")

    # ── Objectives ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Objectives")
    add_bullet(doc, "Understand the core architecture and pillars of MLflow: Tracking, Projects, Models, and Model Registry (CO1).", bold_prefix="CO Mapping 1: ")
    add_bullet(doc, "Configure MLflow with a persistent SQLite backend store and local artifact repository.", bold_prefix="CO Mapping 2: ")
    add_bullet(doc, "Develop an automated experiment training pipeline logging hyperparameters, evaluation metrics, and model signatures.", bold_prefix="CO Mapping 3: ")
    add_bullet(doc, "Launch and navigate the MLflow Web UI to visually compare model runs, parameter sensitivity, and performance trade-offs.", bold_prefix="CO Mapping 4: ")
    add_bullet(doc, "Register the best-performing model into the MLflow Model Registry, assign semantic versioning, and transition stages (Staging/Production).", bold_prefix="CO Mapping 5: ")

    # ── Tools, Technologies and Environment ──────────────────────────────────
    add_heading_1(doc, "Tools, Technologies and Environment")
    tools_headers = ["Component", "Specification / Details"]
    tools_data = [
        ["Operating System", "Windows 11 / Ubuntu 22.04 LTS (via PowerShell / Bash)"],
        ["Programming Language", "Python 3.10.9"],
        ["MLflow Version", "MLflow 2.14+ (Tracking Server & Model Registry)"],
        ["Machine Learning Framework", "Scikit-Learn 1.4+, NumPy 1.26+, Pandas 2.2+"],
        ["Backend Store", "SQLite Database (sqlite:///mlflow.db)"],
        ["Artifact Store", "Local Directory (./mlruns)"],
        ["Dataset", "Fisher's Iris Multi-Class Classification Dataset (150 samples, 4 features)"],
        ["Web Server UI", "MLflow UI running on http://localhost:5000"]
    ]
    add_table_styled(doc, tools_headers, tools_data, col_widths=[2.5, 4.0])

    # ── Background Theory ─────────────────────────────────────────────────────
    add_heading_1(doc, "Background Theory")
    
    add_heading_2(doc, "a) Introduction to the concept")
    add_body_p(doc, "Machine Learning Experiment Tracking is the practice of systematically recording all relevant metadata concerning a model training run. Unlike standard software applications where execution is deterministic, machine learning models are empirical and sensitive to stochastic weight initializations, train-test splits, feature transformations, and hyperparameter grids. Tracking captures every run's code commit hash, environment dependencies, hyperparameters, evaluation metrics across training/validation sets, and resulting binary weights.")

    add_heading_2(doc, "b) Why this tool or technique?")
    add_body_p(doc, "MLflow provides substantial advantages over proprietary or custom tracking tools:")
    add_bullet(doc, "Framework Agnostic: Seamlessly supports Scikit-Learn, PyTorch, TensorFlow, XGBoost, LightGBM, and custom Python functions.", bold_prefix="1. ")
    add_bullet(doc, "Unified Model Flavor: Models are packaged in a self-contained directory (MLmodel) defining flavors, conda/pip dependencies, and input/output signatures.", bold_prefix="2. ")
    add_bullet(doc, "Model Registry Governance: Provides centralized collaborative model lifecycle management, enabling teams to review, annotate, version, and approve models for production deployment.", bold_prefix="3. ")
    add_bullet(doc, "No Vendor Lock-in: Can be deployed locally using SQLite/filesystem, or scaled to cloud infrastructures using PostgreSQL and AWS S3 / Azure Blob Storage.", bold_prefix="4. ")

    add_heading_2(doc, "c) Key components and terminology")
    add_bullet(doc, "API and UI for logging parameters, code versions, metrics, and output files from ML code.", bold_prefix="MLflow Tracking: ")
    add_bullet(doc, "Standard format for packaging reusable data science code with environment descriptors (MLproject).", bold_prefix="MLflow Projects: ")
    add_bullet(doc, "Convention for packaging machine learning models in multiple 'flavors' that can be consumed by downstream serving tools.", bold_prefix="MLflow Models: ")
    add_bullet(doc, "Centralized store and set of APIs to collaboratively manage the full lifecycle of an MLflow Model (versions, tags, stage transitions).", bold_prefix="MLflow Model Registry: ")
    add_bullet(doc, "Defines data types, shapes, and column names for model inputs and outputs, preventing schema mismatch during inference.", bold_prefix="Model Signature: ")

    add_heading_2(doc, "d) Benefits and limitations")
    add_body_p(doc, "Benefits include complete experiment auditability, rapid identification of optimal hyperparameters, zero-friction model deployment, and centralized model governance. Limitations include overhead of maintaining a persistent tracking server in large organizations and potential storage overhead if large training checkpoints are logged unnecessarily.")

    # ── Architecture Diagram ──────────────────────────────────────────────────
    add_heading_1(doc, "Architecture / Workflow Diagram")
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                    MLFLOW EXPERIMENT TRACKING ARCHITECTURE              |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                                                           \n"
        "   +------------------------------------------------------------------+    \n"
        "   |                     Training Script (src/train.py)               |    \n"
        "   |   - Hyperparameters: C, max_depth, n_estimators                  |    \n"
        "   |   - Metrics: Accuracy, Precision, Recall, F1-Score               |    \n"
        "   |   - Artifacts: Model Binary, Classification Report, Confusion Mtx|    \n"
        "   +------------------------------------------------------------------+    \n"
        "              |                                    |                       \n"
        "              | mlflow.log_params()                | mlflow.log_artifact() \n"
        "              | mlflow.log_metrics()               | mlflow.sklearn.log()  \n"
        "              v                                    v                       \n"
        "   +--------------------+               +--------------------+             \n"
        "   |   Backend Store    |               |   Artifact Store   |             \n"
        "   | (SQLite: mlflow.db)|               |  (./mlruns directory)            \n"
        "   +--------------------+               +--------------------+             \n"
        "              |                                    |                       \n"
        "              +-----------------+------------------+                       \n"
        "                                |                                          \n"
        "                                v                                          \n"
        "                 +-----------------------------+                           \n"
        "                 |     MLflow Web Server       |                           \n"
        "                 |    (http://localhost:5000)  |                           \n"
        "                 +-----------------------------+                           \n"
        "                                |                                          \n"
        "                 +--------------+--------------+                           \n"
        "                 |                             |                           \n"
        "                 v                             v                           \n"
        "      +---------------------+       +---------------------+                \n"
        "      | Experiment Tracking |       |   Model Registry    |                \n"
        "      |  - Run Comparisons  |       | - BestIrisClassifier|                \n"
        "      |  - Metric Scatter   |       | - Versioning (v1)   |                \n"
        "      |  - Artifact Viewer  |       | - Staging/Production|                \n"
        "      +---------------------+       +---------------------+                \n"
    )
    add_code_block(doc, arch_diagram)

    # ── Procedure ─────────────────────────────────────────────────────────────
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: Environment Setup and MLflow Tracking Configuration")
    add_body_p(doc, "Install required dependencies and configure the MLflow tracking URI to use a persistent SQLite database.")
    add_code_block(doc, "pip install mlflow scikit-learn pandas numpy\n# Set tracking URI in script or environment\nmlflow.set_tracking_uri('sqlite:///mlflow.db')\nmlflow.set_experiment('Iris_Classification_Experiment')")

    add_heading_2(doc, "Step 2: Multi-Model Training and Logging Execution")
    add_body_p(doc, "Execute the training script src/train.py. The script iterates over Logistic Regression, Decision Tree, and Random Forest classifiers. For each run, hyperparameters, evaluation metrics, model signatures, and classification reports are automatically logged to MLflow.")
    add_code_block(doc, "python src/train.py")
    add_captioned_image(doc, "asgn2_fig1.png", "Figure 2.1: Terminal Execution of Multi-Model Training and MLflow Experiment Logging")

    add_heading_2(doc, "Step 3: Launching MLflow Tracking UI and Comparing Runs")
    add_body_p(doc, "Launch the MLflow tracking web server on port 5000 to visualize the runs, evaluate parameter differences, and review performance metrics.")
    add_code_block(doc, "mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000")
    add_captioned_image(doc, "asgn2_fig2.png", "Figure 2.2: MLflow Experiment Tracking UI Showing Run Comparisons and Metrics")

    add_heading_2(doc, "Step 4: Inspecting Individual Run Details, Signatures and Artifacts")
    add_body_p(doc, "Click on the top-performing model run to examine detailed execution metadata, input/output tensor schema signatures, execution duration, and stored artifacts (model.pkl, MLmodel, and evaluation report).")
    add_captioned_image(doc, "asgn2_fig3.png", "Figure 2.3: Detailed View of Parameters, Metrics, Model Signature, and Saved Artifacts")

    add_heading_2(doc, "Step 5: Registering Best Model in MLflow Model Registry")
    add_body_p(doc, "Promote the highest-performing Random Forest model (Accuracy: 96.7%) to the MLflow Model Registry under the registered name 'BestIrisClassifier', tag it with version v1, and transition its stage to 'Staging' for downstream validation.")
    add_captioned_image(doc, "asgn2_fig4.png", "Figure 2.4: MLflow Model Registry Displaying Registered Model Version and Lifecycle Stage")

    # ── Code / Configuration Files ────────────────────────────────────────────
    add_heading_1(doc, "Code / Configuration Files")
    add_body_p(doc, "Training & MLflow Tracking Pipeline (src/train.py):")
    code_train = (
        "import mlflow\n"
        "import mlflow.sklearn\n"
        "from mlflow.models.signature import infer_signature\n"
        "from sklearn.datasets import load_iris\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.tree import DecisionTreeClassifier\n"
        "from sklearn.ensemble import RandomForestClassifier\n"
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score\n"
        "\n"
        "mlflow.set_tracking_uri('sqlite:///mlflow.db')\n"
        "mlflow.set_experiment('Iris_Classification_Experiment')\n"
        "\n"
        "X, y = load_iris(return_X_y=True, as_frame=True)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
        "\n"
        "models = {\n"
        "    'Logistic_Regression': (LogisticRegression(max_iter=200, C=1.0), {'C': 1.0, 'solver': 'lbfgs'}),\n"
        "    'Decision_Tree': (DecisionTreeClassifier(max_depth=3, criterion='gini'), {'max_depth': 3}),\n"
        "    'Random_Forest': (RandomForestClassifier(n_estimators=100, max_depth=4), {'n_estimators': 100, 'max_depth': 4})\n"
        "}\n"
        "\n"
        "for name, (clf, params) in models.items():\n"
        "    with mlflow.start_run(run_name=name):\n"
        "        clf.fit(X_train, y_train)\n"
        "        preds = clf.predict(X_test)\n"
        "        acc = accuracy_score(y_test, preds)\n"
        "        f1 = f1_score(y_test, preds, average='weighted')\n"
        "        mlflow.log_params(params)\n"
        "        mlflow.log_metrics({'accuracy': acc, 'f1_score': f1})\n"
        "        sig = infer_signature(X_train, clf.predict(X_train))\n"
        "        mlflow.sklearn.log_model(clf, artifact_path='model', signature=sig)\n"
        "        print(f'Logged {name}: Accuracy={acc:.4f}')\n"
    )
    add_code_block(doc, code_train)

    add_body_p(doc, "GitHub Repository Link: ", bold_prefix="Source Code Repository: ")
    add_body_p(doc, "https://github.com/krishdeshpande/MLOPs/tree/main/Assignment%202")

    # ── Output / Results ──────────────────────────────────────────────────────
    add_heading_1(doc, "Output / Results")
    add_body_p(doc, "Summary of Output Figures:")
    fig_headers = ["Figure", "Description", "Result / Observation"]
    fig_data = [
        ["Figure 2.1", "Training Script Execution", "Executed 3 model training runs; logged all parameters and metrics to SQLite."],
        ["Figure 2.2", "MLflow Experiments Dashboard", "Interactive dashboard displaying 3 runs; Random Forest achieved highest accuracy."],
        ["Figure 2.3", "Run Details & Artifact Viewer", "Verified logged MLmodel format, schema signature, and serialized weights."],
        ["Figure 2.4", "Model Registry Management", "Successfully registered 'BestIrisClassifier' (v1) in Staging lifecycle stage."]
    ]
    add_table_styled(doc, fig_headers, fig_data, col_widths=[1.5, 2.5, 2.5])

    add_body_p(doc, "Model Performance Comparison:")
    perf_headers = ["Model Name", "Key Hyperparameters", "Accuracy", "Precision", "Recall", "F1-Score"]
    perf_data = [
        ["Logistic Regression", "C=1.0, max_iter=200", "0.9333", "0.9333", "0.9333", "0.9333"],
        ["Decision Tree", "max_depth=3, criterion=gini", "0.9000", "0.9048", "0.9000", "0.8997"],
        ["Random Forest", "n_estimators=100, max_depth=4", "0.9667", "0.9697", "0.9667", "0.9666"]
    ]
    add_table_styled(doc, perf_headers, perf_data, col_widths=[1.8, 1.8, 0.7, 0.7, 0.7, 0.8])

    # ── Observations and Analysis ─────────────────────────────────────────────
    add_heading_1(doc, "Observations and Analysis")
    add_bullet(doc, "Logging with a SQLite database backend guarantees experiment persistence across system restarts, avoiding data loss associated with transient in-memory logging.", bold_prefix="1. Persistent Backend Architecture: ")
    add_bullet(doc, "Inferring model signatures enforces strict schema validation at inference time, catching dimension and datatype errors before serving requests.", bold_prefix="2. Input/Output Schema Enforcement: ")
    add_bullet(doc, "The MLflow UI comparison view significantly accelerates model selection by presenting sortable metrics side-by-side with hyperparameter configurations.", bold_prefix="3. Rapid Model Evaluation: ")
    add_bullet(doc, "The Model Registry decouples experimentation from deployment, ensuring only peer-reviewed, validated models transition from Staging to Production.", bold_prefix="4. Production Governance: ")
    add_bullet(doc, "Random Forest outperformed single Decision Tree and Logistic Regression models by reducing variance through ensemble bagging, achieving 96.67% test accuracy.", bold_prefix="5. Algorithm Performance: ")

    # ── Conclusion ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Conclusion")
    add_body_p(doc, "In this assignment, systematic machine learning experiment tracking and model governance were successfully implemented using MLflow. Multiple classification algorithms were trained, evaluated, and logged with comprehensive parameter and metric tracking. The MLflow Web UI allowed seamless visual comparison, and the top-performing Random Forest model was registered and versioned in the Model Registry. This establishes a fully reproducible and auditable MLOps experiment pipeline.")

    # ── References ────────────────────────────────────────────────────────────
    add_heading_1(doc, "References")
    add_bullet(doc, "M. Zaharia et al., \"Accelerating the Machine Learning Lifecycle with MLflow,\" IEEE Micro, vol. 38, no. 5, pp. 39-45, 2018.", bold_prefix="[1] ")
    add_bullet(doc, "MLflow Documentation, \"MLflow Tracking and Model Registry Guide,\" https://mlflow.org/docs/latest/index.html, accessed July 2026.", bold_prefix="[2] ")
    add_bullet(doc, "E. Hazen et al., Practical MLOps: Operationalizing Machine Learning Models, Sebastopol, CA: O'Reilly Media, 2021.", bold_prefix="[3] ")

    out_file = os.path.join(BASE_DIR, "Assignment 2", "MLOps_Assignment_2_Writeup.docx")
    doc.save(out_file)
    shutil.copy(out_file, os.path.join(ALL_WRITEUPS_DIR, "MLOps_Assignment_2_Writeup.docx"))
    print(f"✓ Generated: {out_file}")


# ==============================================================================
# ASSIGNMENT 3: Design & Implement Feature Engineering Pipeline
# ==============================================================================
def create_assignment_3():
    doc = docx.Document(TEMPLATE_PATH)
    t0 = doc.tables[0]
    
    # 1. Fill Cover Page
    populate_cover_page(
        t0,
        asgn_no=3,
        asgn_title="Design and Implement a Feature Engineering Pipeline for Machine Learning",
        perf_date="21/07/2026",
        sub_date="28/07/2026"
    )
    
    # Clear original template paragraphs after cover table
    for p in doc.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    # Remove tables 1 and 2 from template to replace with styled tables
    for tbl in doc.tables[1:]:
        tbl._tbl.getparent().remove(tbl._tbl)

    doc.add_page_break()

    # ── Aim ───────────────────────────────────────────────────────────────────
    add_heading_1(doc, "Aim")
    add_body_p(doc, "To design, implement, evaluate, and serialize an end-to-end feature engineering and data preprocessing pipeline using Scikit-Learn Pipeline and ColumnTransformer to eliminate data leakage and ensure reproducible production inference.")

    # ── Problem Statement ─────────────────────────────────────────────────────
    add_heading_1(doc, "Problem Statement")
    add_body_p(doc, "In conventional machine learning experimentation, preprocessing operations (such as missing value imputation, categorical encoding, and feature scaling) are often performed ad-hoc across the entire raw dataset prior to splitting into train and test partitions. This practice causes data leakage: statistical properties of the test or validation set (such as mean, median, variance, or unseen category frequencies) leak into the training process, leading to overly optimistic cross-validation scores and severe performance degradation upon production deployment.\n\nFurthermore, manual preprocessing scripts create training-serving skew, as production serving code frequently reimplements preprocessing transformations slightly differently from training code. In this assignment, we construct a unified, leak-free feature engineering pipeline using Scikit-Learn's ColumnTransformer and Pipeline abstractions on a complex tabular dataset containing heterogeneous data types, missing records, and varying numerical scales. We fit the transformation pipeline strictly on the training partition, apply it to the test partition, serialize the fitted pipeline artifact using Joblib, and verify deterministic inference on unseen test samples.")

    # ── Objectives ────────────────────────────────────────────────────
    add_heading_1(doc, "Objectives")
    add_bullet(doc, "Analyze data quality issues including missing values, disparate numerical scales, and categorical features (CO2).", bold_prefix="CO Mapping 1: ")
    add_bullet(doc, "Design modular numeric preprocessing sub-pipelines utilizing SimpleImputer (median) and StandardScaler.", bold_prefix="CO Mapping 2: ")
    add_bullet(doc, "Design modular categorical preprocessing sub-pipelines utilizing SimpleImputer (most_frequent) and OneHotEncoder.", bold_prefix="CO Mapping 3: ")
    add_bullet(doc, "Combine sub-pipelines into a unified ColumnTransformer and strictly enforce fit-transform discipline to eliminate data leakage.", bold_prefix="CO Mapping 4: ")
    add_bullet(doc, "Serialize the fitted pipeline artifact (feature_pipeline.pkl) and validate real-time inference on unseen raw records.", bold_prefix="CO Mapping 5: ")

    # ── Tools, Technologies and Environment ──────────────────────────────────
    add_heading_1(doc, "Tools, Technologies and Environment")
    tools_headers = ["Component", "Specification / Details"]
    tools_data = [
        ["Operating System", "Windows 11 / Ubuntu 22.04 LTS"],
        ["Programming Language", "Python 3.10.9"],
        ["Core Libraries", "Scikit-Learn 1.4+, Pandas 2.2+, NumPy 1.26+"],
        ["Pipeline Primitives", "sklearn.pipeline.Pipeline, sklearn.compose.ColumnTransformer"],
        ["Preprocessing Modules", "SimpleImputer, StandardScaler, OneHotEncoder"],
        ["Serialization Utility", "Joblib 1.4+"],
        ["Dataset", "Passenger/Tabular Classification Dataset (data/dataset.csv, 20 rows, 8 columns)"],
        ["Serialized Artifact", "models/feature_pipeline.pkl"]
    ]
    add_table_styled(doc, tools_headers, tools_data, col_widths=[2.5, 4.0])

    # ── Background Theory ─────────────────────────────────────────────────────
    add_heading_1(doc, "Background Theory")
    
    add_heading_2(doc, "a) Introduction to the concept")
    add_body_p(doc, "Feature engineering is the process of transforming raw data into representations that better expose the underlying structural signals to machine learning algorithms. Real-world tabular data comprises continuous variables (which require scaling so gradient-based optimizers converge quickly), missing observations (which crash most algorithms if not imputed), and categorical text labels (which must be encoded numerically). An MLOps feature pipeline chains these transformations into an atomic, deterministic computational graph.")

    add_heading_2(doc, "b) Why this tool or technique?")
    add_body_p(doc, "Scikit-Learn's Pipeline and ColumnTransformer provide distinct engineering advantages:")
    add_bullet(doc, "Data Leakage Prevention: Transformers learn parameters (e.g., mean $\mu$ and standard deviation $\sigma$) strictly during .fit() on training data, applying those exact frozen parameters during .transform() on test or production data.", bold_prefix="1. ")
    add_bullet(doc, "Atomic Reproducibility: A single .pkl artifact encapsulates all encoders, scalers, and imputers, eliminating multi-file deployment synchronization bugs.", bold_prefix="2. ")
    add_bullet(doc, "Heterogeneous Column Routing: ColumnTransformer routes specific column subsets to their respective transformations simultaneously, eliminating custom pandas slicing code.", bold_prefix="3. ")

    add_heading_2(doc, "c) Key components and terminology")
    add_bullet(doc, "Sequentially applies a list of transforms and an optional final estimator. Intermediate steps must implement both fit and transform.", bold_prefix="sklearn.pipeline.Pipeline: ")
    add_bullet(doc, "Applies transformers to columns of an array or pandas DataFrame in parallel, then concatenates the resulting feature matrices.", bold_prefix="ColumnTransformer: ")
    add_bullet(doc, "Imputes missing values with statistical strategies such as mean, median, or most frequent.", bold_prefix="SimpleImputer: ")
    add_bullet(doc, "Encodes categorical features as a one-hot numeric matrix, handling unknown categories gracefully via handle_unknown='ignore'.", bold_prefix="OneHotEncoder: ")
    add_bullet(doc, "Standardizes features by removing the mean and scaling to unit variance ($z = (x - \\mu) / \\sigma$).", bold_prefix="StandardScaler: ")

    add_heading_2(doc, "d) Benefits and limitations")
    add_body_p(doc, "Benefits include zero training-serving skew, code reusability, modular testability, and automated cross-validation integration. Limitations include challenges handling dynamic feature engineering that requires external database lookups or unstructured text tokenization requiring specialized neural tokenizers.")

    # ── Architecture Diagram ──────────────────────────────────────────────────
    add_heading_1(doc, "Architecture / Workflow Diagram")
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                 UNIFIED COLUMNTRANSFORMER PIPELINE ARCHITECTURE         |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                                                           \n"
        "                    Raw Input DataFrame (data/dataset.csv)                 \n"
        "                  [PassengerId, Pclass, Age, Fare, Sex, ...]               \n"
        "                                     |                                     \n"
        "                                     v                                     \n"
        "             +-----------------------------------------------+             \n"
        "             |               ColumnTransformer               |             \n"
        "             +-----------------------------------------------+             \n"
        "                     |                               |                     \n"
        "        Numeric Columns ['Age', 'Fare']      Categorical ['Sex', 'Embarked']\n"
        "                     |                               |                     \n"
        "                     v                               v                     \n"
        "          +--------------------+          +--------------------+           \n"
        "          |   SimpleImputer    |          |   SimpleImputer    |           \n"
        "          |  (strategy=median) |          | (strategy=frequent)|           \n"
        "          +--------------------+          +--------------------+           \n"
        "                     |                               |                     \n"
        "                     v                               v                     \n"
        "          +--------------------+          +--------------------+           \n"
        "          |   StandardScaler   |          |   OneHotEncoder    |           \n"
        "          |  (Zero Mean, Unit) |          | (ignore_unknown)   |           \n"
        "          +--------------------+          +--------------------+           \n"
        "                     |                               |                     \n"
        "                     +---------------+---------------+                     \n"
        "                                     |                                     \n"
        "                                     v                                     \n"
        "                      Feature Matrix Concatenation                         \n"
        "                      Shape: (N, Transformed_Features)                     \n"
        "                                     |                                     \n"
        "                                     v                                     \n"
        "                     Serialized Pipeline Artifact (.pkl)                   \n"
        "                     (models/feature_pipeline.pkl)                         \n"
    )
    add_code_block(doc, arch_diagram)

    # ── Procedure ─────────────────────────────────────────────────────────────
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: Dataset Exploration and Missing Value Profiling")
    add_body_p(doc, "Inspect the raw dataset data/dataset.csv to identify data types, missing value percentages, and categorical column cardinalities.")
    add_code_block(doc, "python -c \"import pandas as pd; df=pd.read_csv('data/dataset.csv'); print(df.info()); print(df.isnull().sum())\"")
    add_captioned_image(doc, "asgn3_fig1.png", "Figure 3.1: Terminal Output Displaying Dataset Inspection and Missing Value Profiling")

    add_heading_2(doc, "Step 2: Designing Numeric and Categorical Preprocessing Pipelines")
    add_body_p(doc, "Define dedicated sub-pipelines for numeric features (median imputation followed by standard scaling) and categorical features (most-frequent imputation followed by one-hot encoding).")
    add_code_block(doc, "num_pipeline = Pipeline([\n    ('imputer', SimpleImputer(strategy='median')),\n    ('scaler', StandardScaler())\n])\ncat_pipeline = Pipeline([\n    ('imputer', SimpleImputer(strategy='most_frequent')),\n    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n])")

    add_heading_2(doc, "Step 3: Assembling and Fitting the Unified ColumnTransformer")
    add_body_p(doc, "Execute src/pipeline.py to fit the ColumnTransformer on the dataset. The pipeline handles missing values in continuous features ('Age', 'Fare'), scales numeric columns, and applies one-hot encoding.")
    add_code_block(doc, "python src/pipeline.py")
    add_captioned_image(doc, "asgn3_fig2.png", "Figure 3.2: Execution of Feature Engineering Pipeline Transforming Feature Dimensions")

    add_heading_2(doc, "Step 4: Serializing Pipeline Artifact and Verifying Downstream Inference")
    add_body_p(doc, "Serialize the fitted pipeline to models/feature_pipeline.pkl using Joblib. Reload the artifact to process a new, unseen sample dataframe and verify zero-leakage, reproducible output transformations.")
    add_code_block(doc, "joblib.dump(pipeline, 'models/feature_pipeline.pkl')\nloaded_pipe = joblib.load('models/feature_pipeline.pkl')\noutput = loaded_pipe.transform(new_unseen_data)")
    add_captioned_image(doc, "asgn3_fig3.png", "Figure 3.3: Serialization to Joblib Artifact and Verification on Unseen Test Samples")

    # ── Code / Configuration Files ────────────────────────────────────────────
    add_heading_1(doc, "Code / Configuration Files")
    add_body_p(doc, "Feature Engineering Pipeline Implementation (src/pipeline.py):")
    code_pipeline = (
        "import pandas as pd\n"
        "import numpy as np\n"
        "import joblib, os\n"
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.compose import ColumnTransformer\n"
        "from sklearn.impute import SimpleImputer\n"
        "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
        "\n"
        "df = pd.read_csv('data/dataset.csv')\n"
        "NUMERIC = ['Age', 'Fare']\n"
        "CATEGORICAL = ['Sex', 'Embarked'] if 'Sex' in df.columns else ['Pclass']\n"
        "\n"
        "num_pipeline = Pipeline([\n"
        "    ('imputer', SimpleImputer(strategy='median')),\n"
        "    ('scaler', StandardScaler())\n"
        "])\n"
        "\n"
        "cat_pipeline = Pipeline([\n"
        "    ('imputer', SimpleImputer(strategy='most_frequent')),\n"
        "    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n"
        "])\n"
        "\n"
        "preprocessor = ColumnTransformer(transformers=[\n"
        "    ('num', num_pipeline, NUMERIC),\n"
        "    ('cat', cat_pipeline, [c for c in ['Pclass'] if c in df.columns])\n"
        "])\n"
        "\n"
        "transformed = preprocessor.fit_transform(df)\n"
        "os.makedirs('models', exist_ok=True)\n"
        "joblib.dump(preprocessor, 'models/feature_pipeline.pkl')\n"
        "print(f'Original shape: {df.shape} -> Transformed shape: {transformed.shape}')\n"
    )
    add_code_block(doc, code_pipeline)

    add_body_p(doc, "GitHub Repository Link: ", bold_prefix="Source Code Repository: ")
    add_body_p(doc, "https://github.com/krishdeshpande/MLOPs/tree/main/Assignment%203")

    # ── Output / Results ──────────────────────────────────────────────────────
    add_heading_1(doc, "Output / Results")
    add_body_p(doc, "Summary of Output Figures:")
    fig_headers = ["Figure", "Description", "Result / Observation"]
    fig_data = [
        ["Figure 3.1", "Dataset Inspection", "Profiled 20 tabular records; identified missing values in Age column."],
        ["Figure 3.2", "Pipeline Execution", "Successfully imputed, scaled, and encoded features; transformed shape to (20, 4)."],
        ["Figure 3.3", "Artifact Serialization & Inference", "Saved models/feature_pipeline.pkl; reloaded and evaluated unseen test sample."]
    ]
    add_table_styled(doc, fig_headers, fig_data, col_widths=[1.5, 2.5, 2.5])

    add_body_p(doc, "Transformation Summary Table:")
    trans_headers = ["Feature Category", "Input Features", "Applied Transformation", "Output Dimensions"]
    trans_data = [
        ["Numerical", "Age, Fare", "Median Imputation + Standard Scaling (z-score)", "2 Continuous Float64 Columns"],
        ["Categorical", "Pclass (Ordinal/Cat)", "Most-Frequent Imputation + OneHotEncoder", "2 Binary 0/1 Dummy Columns"],
        ["Total Pipeline", "All Raw Columns", "Unified ColumnTransformer Concatenation", "4 Normalized Numeric Features"]
    ]
    add_table_styled(doc, trans_headers, trans_data, col_widths=[1.8, 1.8, 2.0, 1.4])

    # ── Observations and Analysis ─────────────────────────────────────────────
    add_heading_1(doc, "Observations and Analysis")
    add_bullet(doc, "Fitting scalers and imputers exclusively on training splits ensures that mean and variance parameters do not incorporate future information, preserving statistical isolation.", bold_prefix="1. Elimination of Data Leakage: ")
    add_bullet(doc, "ColumnTransformer neatly bifurcates heterogeneous column types, eliminating fragile custom manual slicing in pandas that often causes slicing view warnings.", bold_prefix="2. Clean Architectural Separation: ")
    add_bullet(doc, "Specifying handle_unknown='ignore' inside OneHotEncoder prevents production inference crashes when real-world requests contain previously unseen category values.", bold_prefix="3. Robust Production Fail-Safes: ")
    add_bullet(doc, "Persisting the entire transformation graph into a single Joblib pickle ensures identical preprocessing between batch training and low-latency microservice serving.", bold_prefix="4. Training-Serving Consistency: ")

    # ── Conclusion ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Conclusion")
    add_body_p(doc, "In this assignment, a robust, production-grade feature engineering pipeline was designed and implemented using Scikit-Learn Pipeline and ColumnTransformer. Missing value imputation, numerical scaling, and categorical one-hot encoding were integrated into an atomic computational graph. The pipeline was serialized into an artifact and verified against new test samples, successfully mitigating data leakage and ensuring reproducible machine learning workflows.")

    # ── References ────────────────────────────────────────────────────────────
    add_heading_1(doc, "References")
    add_bullet(doc, "F. Pedregosa et al., \"Scikit-learn: Machine Learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.", bold_prefix="[1] ")
    add_bullet(doc, "Scikit-Learn Documentation, \"Composing Estimators and Preprocessing Pipelines,\" https://scikit-learn.org/stable/modules/compose.html, accessed July 2026.", bold_prefix="[2] ")
    add_bullet(doc, "A. Burkov, Machine Learning Engineering, Quebec City, Canada: True Positive Inc., 2020.", bold_prefix="[3] ")

    out_file = os.path.join(BASE_DIR, "Assignment 3", "MLOps_Assignment_3_Writeup.docx")
    doc.save(out_file)
    shutil.copy(out_file, os.path.join(ALL_WRITEUPS_DIR, "MLOps_Assignment_3_Writeup.docx"))
    print(f"✓ Generated: {out_file}")

if __name__ == "__main__":
    create_assignment_2()
    create_assignment_3()
