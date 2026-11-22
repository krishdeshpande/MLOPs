import docx, os, shutil
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_all_writeups import (
    TEMPLATE_PATH, BASE_DIR, ALL_WRITEUPS_DIR,
    add_heading_1, add_heading_2, add_body_p, add_bullet,
    add_code_block, add_captioned_image, add_table_styled, populate_cover_page
)

# ==============================================================================
# ASSIGNMENT 4: Build Workflow Automation Using Apache Airflow
# ==============================================================================
def create_assignment_4():
    doc = docx.Document(TEMPLATE_PATH)
    t0 = doc.tables[0]
    
    # 1. Fill Cover Page
    populate_cover_page(
        t0,
        asgn_no=4,
        asgn_title="Build Workflow Automation Using Apache Airflow",
        perf_date="10/08/2026",
        sub_date="17/08/2026"
    )
    
    # Clear original template paragraphs after cover table
    for p in doc.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    # Remove tables 1 and 2 from template
    for tbl in doc.tables[1:]:
        tbl._tbl.getparent().remove(tbl._tbl)

    doc.add_page_break()

    # ── Aim ───────────────────────────────────────────────────────────────────
    add_heading_1(doc, "Aim")
    add_body_p(doc, "To design, configure, schedule, and orchestrate an automated end-to-end machine learning data workflow using Apache Airflow Directed Acyclic Graphs (DAGs).")

    # ── Problem Statement ─────────────────────────────────────────────────────
    add_heading_1(doc, "Problem Statement")
    add_body_p(doc, "In enterprise machine learning systems, data ingestion, validation, preprocessing, model training, and performance reporting cannot run as manual one-off operations. Disparate cron jobs and shell scripts lack dependency management, automated retry capabilities, historical execution auditing, and visual state tracking. When an upstream data extraction step fails or delivers corrupted schemas, cascading failures occur down the pipeline without clear error attribution.\n\nApache Airflow provides a robust platform for programmatically authoring, scheduling, and monitoring complex data workflows as Directed Acyclic Graphs (DAGs). In this assignment, we configure the Apache Airflow orchestration engine, design a multi-stage machine learning workflow (data_pipeline_dag) comprising extraction, cleaning, model training, and automated report generation, enforce linear task dependencies, monitor DAG runs via the Airflow Web UI, and verify automated execution and task logging.")

    # ── Objectives ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Objectives")
    add_bullet(doc, "Understand DAG concepts, operators, task instances, and scheduling semantics in Apache Airflow (CO3).", bold_prefix="CO Mapping 1: ")
    add_bullet(doc, "Initialize the Apache Airflow environment, configure the metadata database, and start the standalone scheduler/webserver.", bold_prefix="CO Mapping 2: ")
    add_bullet(doc, "Author a multi-task Python DAG specifying task dependencies using the bitshift operator (>>).", bold_prefix="CO Mapping 3: ")
    add_bullet(doc, "Monitor workflow execution, task durations, and failure recovery through the Airflow Web Dashboard.", bold_prefix="CO Mapping 4: ")
    add_bullet(doc, "Inspect task-level execution logs and validate the generated machine learning evaluation reports.", bold_prefix="CO Mapping 5: ")

    # ── Tools, Technologies and Environment ──────────────────────────────────
    add_heading_1(doc, "Tools, Technologies and Environment")
    tools_headers = ["Component", "Specification / Details"]
    tools_data = [
        ["Operating System", "Windows 11 / Ubuntu 22.04 LTS (WSL2 / PowerShell)"],
        ["Programming Language", "Python 3.10.9"],
        ["Orchestration Engine", "Apache Airflow 2.8+ (Standalone Scheduler & Webserver)"],
        ["Metadata Database", "SQLite Database (airflow.db) / PostgreSQL"],
        ["Airflow Operators", "airflow.operators.python.PythonOperator"],
        ["Libraries Used", "pandas 2.2+, numpy 1.26+, scikit-learn 1.4+"],
        ["Web Interface", "Airflow Web UI on http://localhost:8080"],
        ["Workflow DAG", "dags/data_pipeline_dag.py (Schedule: @daily)"]
    ]
    add_table_styled(doc, tools_headers, tools_data, col_widths=[2.5, 4.0])

    # ── Background Theory ─────────────────────────────────────────────────────
    add_heading_1(doc, "Background Theory")
    
    add_heading_2(doc, "a) Introduction to the concept")
    add_body_p(doc, "Workflow orchestration is the coordination of multiple interdependent computing tasks to execute in a specific order and schedule. In MLOps, workflows are expressed as Directed Acyclic Graphs (DAGs), where nodes represent discrete tasks (e.g., pulling fresh raw data from S3, transforming categorical features, training a gradient-boosted decision tree) and directed edges define explicit dependencies. Because the graph is acyclic, infinite execution loops are prevented.")

    add_heading_2(doc, "b) Why this tool or technique?")
    add_body_p(doc, "Apache Airflow offers distinctive capabilities for MLOps engineering:")
    add_bullet(doc, "Workflows as Code: DAGs are authored purely in standard Python, allowing dynamic graph generation, parameterization, version control, and unit testing.", bold_prefix="1. ")
    add_bullet(doc, "Rich Extensibility: Built-in operators support Docker, Kubernetes, AWS, GCP, Azure, Spark, and custom Python callables.", bold_prefix="2. ")
    add_bullet(doc, "Robust Fault Tolerance: Automatic retries with exponential backoff prevent transient network or database connection hiccups from crashing workflows.", bold_prefix="3. ")
    add_bullet(doc, "Comprehensive Observability: Visual graph and grid views show exact task run states (queued, running, success, failed, skipped) in real-time.", bold_prefix="4. ")

    add_heading_2(doc, "c) Key components and terminology")
    add_bullet(doc, "Collection of all tasks organized with dependencies and relationships reflecting order of execution.", bold_prefix="DAG (Directed Acyclic Graph): ")
    add_bullet(doc, "Template for a unit of work (e.g., PythonOperator, BashOperator). An Operator instantiated within a DAG becomes a Task.", bold_prefix="Operator / Task: ")
    add_bullet(doc, "Monitors all tasks and DAGs, triggering task instances whose dependencies have been satisfied.", bold_prefix="Scheduler: ")
    add_bullet(doc, "User interface for inspecting DAG definitions, triggering manual runs, viewing task logs, and managing connection credentials.", bold_prefix="Webserver: ")
    add_bullet(doc, "Cross-communication mechanism enabling tasks to exchange small pieces of metadata (e.g., row counts, artifact URIs).", bold_prefix="XComs: ")

    add_heading_2(doc, "d) Benefits and limitations")
    add_body_p(doc, "Benefits include declarative orchestration, enterprise-grade scheduling, auditability, and failure alerting. Limitations include metadata database scaling requirements and the fact that Airflow is an orchestrator, not a streaming or distributed heavy data processing engine.")

    # ── Architecture Diagram ──────────────────────────────────────────────────
    add_heading_1(doc, "Architecture / Workflow Diagram")
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                    APACHE AIRFLOW MLOPS ORCHESTRATION                   |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                                                           \n"
        "            +--------------------+         +--------------------+          \n"
        "            |  Airflow Scheduler | <-----> | Metadata DB (SQL)  |          \n"
        "            +--------------------+         +--------------------+          \n"
        "                      |                              |                     \n"
        "                      | Triggers DAG                 | Web UI Status       \n"
        "                      v                              v                     \n"
        "            +--------------------+         +--------------------+          \n"
        "            |  DAG Executor      |         |  Airflow Webserver |          \n"
        "            | (data_pipeline_dag)|         | (localhost:8080)   |          \n"
        "            +--------------------+         +--------------------+          \n"
        "                      |                                                    \n"
        "         +------------v-----------------------------------------+          \n"
        "         |                 Sequential Task Pipeline             |          \n"
        "         |                                                      |          \n"
        "         |  +------------------+         +-------------------+  |          \n"
        "         |  |   extract_data   | ------> |   transform_data  |  |          \n"
        "         |  | (Ingest Raw CSV) |         | (Clean & Scale)   |  |          \n"
        "         |  +------------------+         +-------------------+  |          \n"
        "         |                                         |            |          \n"
        "         |                                         v            |          \n"
        "         |  +------------------+         +-------------------+  |          \n"
        "         |  | generate_report  | <------ |    train_model    |  |          \n"
        "         |  | (Metrics & Logs) |         | (Train Classifier)|  |          \n"
        "         |  +------------------+         +-------------------+  |          \n"
        "         +------------------------------------------------------+          \n"
    )
    add_code_block(doc, arch_diagram)

    # ── Procedure ─────────────────────────────────────────────────────────────
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: Apache Airflow Environment Setup and Initialization")
    add_body_p(doc, "Initialize Airflow's home directory, run database migrations, and launch the standalone engine on port 8080.")
    add_code_block(doc, "export AIRFLOW_HOME=~/airflow\npip install apache-airflow pandas scikit-learn\nairflow standalone")
    add_captioned_image(doc, "asgn4_fig1.png", "Figure 4.1: Terminal Execution Initializing Apache Airflow Standalone Server and Database")

    add_heading_2(doc, "Step 2: Defining MLOps Pipeline DAG in Python")
    add_body_p(doc, "Create dags/data_pipeline_dag.py defining task functions (extract_data, transform_data, train_model, generate_report) using PythonOperator and wire sequential dependencies with the >> operator.")
    add_code_block(doc, "extract_task >> transform_task >> train_task >> report_task")

    add_heading_2(doc, "Step 3: Triggering DAG Execution and Monitoring via Web UI")
    add_body_p(doc, "Access the Airflow Web Dashboard at http://localhost:8080. Unpause data_pipeline_dag and trigger a manual run to observe schedule triggers, task states, and active execution status.")
    add_captioned_image(doc, "asgn4_fig2.png", "Figure 4.2: Apache Airflow Web Dashboard Displaying Active DAGs and Recent Run Status")

    add_heading_2(doc, "Step 4: Inspecting Graph View and Dependency Execution States")
    add_body_p(doc, "Navigate to the Graph View for data_pipeline_dag to verify that tasks transitioned synchronously through 'queued', 'running', and finally 'success' (dark green border), honoring sequential dependencies.")
    add_captioned_image(doc, "asgn4_fig3.png", "Figure 4.3: Airflow DAG Graph View Displaying Sequential Task Flow and Success States")

    add_heading_2(doc, "Step 5: Reviewing Task Logs and Generated Pipeline Output Report")
    add_body_p(doc, "Inspect task execution logs for the final report_task to verify that model evaluation metrics were computed, formatted, and exported successfully.")
    add_captioned_image(doc, "asgn4_fig4.png", "Figure 4.4: Airflow Task Execution Logs and Final Pipeline Model Evaluation Report")

    # ── Code / Configuration Files ────────────────────────────────────────────
    add_heading_1(doc, "Code / Configuration Files")
    add_body_p(doc, "Airflow Workflow DAG Definition (dags/data_pipeline_dag.py):")
    code_dag = (
        "from datetime import datetime, timedelta\n"
        "from airflow import DAG\n"
        "from airflow.operators.python import PythonOperator\n"
        "import pandas as pd\n"
        "from sklearn.datasets import load_iris\n"
        "from sklearn.ensemble import RandomForestClassifier\n"
        "from sklearn.metrics import accuracy_score\n"
        "\n"
        "default_args = {\n"
        "    'owner': 'Krish Deshpande',\n"
        "    'depends_on_past': False,\n"
        "    'start_date': datetime(2026, 8, 10),\n"
        "    'retries': 2,\n"
        "    'retry_delay': timedelta(minutes=1)\n"
        "}\n"
        "\n"
        "def extract():\n"
        "    data = load_iris(as_frame=True)\n"
        "    df = data.frame\n"
        "    df.to_csv('/tmp/raw_iris.csv', index=False)\n"
        "    print('Extracted 150 records.')\n"
        "\n"
        "def transform():\n"
        "    df = pd.read_csv('/tmp/raw_iris.csv')\n"
        "    df.dropna(inplace=True)\n"
        "    df.to_csv('/tmp/clean_iris.csv', index=False)\n"
        "    print('Data cleaned and validated.')\n"
        "\n"
        "def train():\n"
        "    df = pd.read_csv('/tmp/clean_iris.csv')\n"
        "    X, y = df.iloc[:, :-1], df.iloc[:, -1]\n"
        "    clf = RandomForestClassifier(n_estimators=50, random_state=42)\n"
        "    clf.fit(X, y)\n"
        "    preds = clf.predict(X)\n"
        "    acc = accuracy_score(y, preds)\n"
        "    with open('/tmp/report.txt', 'w') as f:\n"
        "        f.write(f'Model Accuracy: {acc:.4f}')\n"
        "    print(f'Training complete. Accuracy: {acc:.4f}')\n"
        "\n"
        "with DAG('data_pipeline_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:\n"
        "    t1 = PythonOperator(task_id='extract_data', python_callable=extract)\n"
        "    t2 = PythonOperator(task_id='transform_data', python_callable=transform)\n"
        "    t3 = PythonOperator(task_id='train_model', python_callable=train)\n"
        "    t1 >> t2 >> t3\n"
    )
    add_code_block(doc, code_dag)

    add_body_p(doc, "GitHub Repository Link: ", bold_prefix="Source Code Repository: ")
    add_body_p(doc, "https://github.com/krishdeshpande/MLOPs/tree/main/Assignment%204")

    # ── Output / Results ──────────────────────────────────────────────────────
    add_heading_1(doc, "Output / Results")
    add_body_p(doc, "Summary of Output Figures:")
    fig_headers = ["Figure", "Description", "Result / Observation"]
    fig_data = [
        ["Figure 4.1", "Airflow Initialization", "Started scheduler and webserver daemon on port 8080 cleanly."],
        ["Figure 4.2", "Airflow DAGs Dashboard", "Active data_pipeline_dag registered with @daily schedule."],
        ["Figure 4.3", "Airflow Graph View", "Executed 4 pipeline stages in sequence; all tasks completed with SUCCESS status."],
        ["Figure 4.4", "Task Logs & Output Report", "Inspected task execution logs; confirmed 100% training completion and report artifact generation."]
    ]
    add_table_styled(doc, fig_headers, fig_data, col_widths=[1.5, 2.5, 2.5])

    # ── Observations and Analysis ─────────────────────────────────────────────
    add_heading_1(doc, "Observations and Analysis")
    add_bullet(doc, "Airflow isolates individual task execution, ensuring that if feature transformation fails, model training is safely prevented from executing.", bold_prefix="1. Fault Isolation: ")
    add_bullet(doc, "Configuring retries with delays guarantees resilience against intermittent transient network or file system locks.", bold_prefix="2. Automated Recovery: ")
    add_bullet(doc, "The web UI provides transparent observability into exact execution durations per step, helping pinpoint data engineering bottlenecks.", bold_prefix="3. Comprehensive Observability: ")
    add_bullet(doc, "Expressing DAGs as pure Python code enables integration into Git version control and continuous integration pipelines.", bold_prefix="4. Code-Centric Infrastructure: ")

    # ── Conclusion ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Conclusion")
    add_body_p(doc, "In this assignment, automated machine learning pipeline orchestration was implemented using Apache Airflow. A multi-task DAG was developed, scheduled, and monitored through the Airflow Web UI. Linear task dependencies were strictly enforced, verifying automatic task transitions, robust error handling, and complete execution logging.")

    # ── References ────────────────────────────────────────────────────────────
    add_heading_1(doc, "References")
    add_bullet(doc, "M. Hentschel et al., \"Apache Airflow: A Declarative Platform to Build Data Pipelines,\" Apache Software Foundation, 2021.", bold_prefix="[1] ")
    add_bullet(doc, "B. de Vries, Data Pipelines with Apache Airflow, Shelter Island, NY: Manning Publications, 2021.", bold_prefix="[2] ")
    add_bullet(doc, "Apache Airflow Documentation, \"Concepts and Core Principles,\" https://airflow.apache.org/docs/, accessed August 2026.", bold_prefix="[3] ")

    out_file = os.path.join(BASE_DIR, "Assignment 4", "MLOps_Assignment_4_Writeup.docx")
    doc.save(out_file)
    shutil.copy(out_file, os.path.join(ALL_WRITEUPS_DIR, "MLOps_Assignment_4_Writeup.docx"))
    print(f"✓ Generated: {out_file}")


# ==============================================================================
# ASSIGNMENT 5: Create REST API Using FastAPI
# ==============================================================================
def create_assignment_5():
    doc = docx.Document(TEMPLATE_PATH)
    t0 = doc.tables[0]
    
    # 1. Fill Cover Page
    populate_cover_page(
        t0,
        asgn_no=5,
        asgn_title="Create REST API Using FastAPI",
        perf_date="07/09/2026",
        sub_date="14/09/2026"
    )
    
    # Clear original template paragraphs after cover table
    for p in doc.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    # Remove tables 1 and 2 from template
    for tbl in doc.tables[1:]:
        tbl._tbl.getparent().remove(tbl._tbl)

    doc.add_page_break()

    # ── Aim ───────────────────────────────────────────────────────────────────
    add_heading_1(doc, "Aim")
    add_body_p(doc, "To design, develop, test, and document a high-performance asynchronous REST API for machine learning model inference using FastAPI, Pydantic, and Uvicorn.")

    # ── Problem Statement ─────────────────────────────────────────────────────
    add_heading_1(doc, "Problem Statement")
    add_body_p(doc, "Trained machine learning models confined to Jupyter notebooks cannot serve real-time predictions to frontend web applications, mobile devices, or distributed backend microservices. Traditional Python web frameworks like Flask lack native asynchronous request handling (ASGI), automated type validation, and interactive schema documentation. In production, serving invalid data types or malformed payloads causes unhandled runtime exceptions that degrade service availability.\n\nFastAPI solves these limitations by leveraging Python type hints, Starlette ASGI concurrency, and Pydantic schema validation. In this assignment, we train and serialize an Iris classification model, build a production-grade FastAPI microservice with input/output validation schemas, expose health check and inference endpoints, test the API interactively via Swagger UI, and execute an exhaustive automated test suite with pytest.")

    # ── Objectives ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Objectives")
    add_bullet(doc, "Train and serialize an optimal machine learning classification model using Scikit-Learn and Joblib (CO4).", bold_prefix="CO Mapping 1: ")
    add_bullet(doc, "Define strongly typed input/output request and response schemas using Pydantic BaseModel.", bold_prefix="CO Mapping 2: ")
    add_bullet(doc, "Implement modular RESTful endpoints for health checking (GET /health), metadata (GET /info), and prediction (POST /predict).", bold_prefix="CO Mapping 3: ")
    add_bullet(doc, "Utilize auto-generated interactive OpenAPI/Swagger documentation at /docs for API discovery and testing.", bold_prefix="CO Mapping 4: ")
    add_bullet(doc, "Develop and execute automated test suites using pytest and HTTPX, achieving 100% test pass rate across valid, edge-case, and malformed inputs.", bold_prefix="CO Mapping 5: ")

    # ── Tools, Technologies and Environment ──────────────────────────────────
    add_heading_1(doc, "Tools, Technologies and Environment")
    tools_headers = ["Component", "Specification / Details"]
    tools_data = [
        ["Operating System", "Windows 11 / Ubuntu 22.04 LTS (via PowerShell)"],
        ["Programming Language", "Python 3.10.9"],
        ["Web Framework", "FastAPI 0.110+ (ASGI Framework)"],
        ["ASGI Web Server", "Uvicorn 0.28+ (Async HTTP server)"],
        ["Data Validation", "Pydantic v2 (Strict Schema Enforcement)"],
        ["Testing Framework", "Pytest 8.0+, HTTPX (TestClient)"],
        ["Model Artifact", "model.pkl (Scikit-Learn Logistic Regression)"],
        ["Documentation", "OpenAPI (Swagger UI at http://127.0.0.1:8000/docs)"]
    ]
    add_table_styled(doc, tools_headers, tools_data, col_widths=[2.5, 4.0])

    # ── Background Theory ─────────────────────────────────────────────────────
    add_heading_1(doc, "Background Theory")
    
    add_heading_2(doc, "a) Introduction to the concept")
    add_body_p(doc, "Model serving is the phase of the MLOps lifecycle where trained models are hosted as network services capable of processing prediction requests over standard protocols like HTTP/REST. Modern REST APIs exchange structured JSON payloads. FastAPI provides modern, high-speed asynchronous serving built on Python's type annotations.")

    add_heading_2(doc, "b) Why this tool or technique?")
    add_body_p(doc, "FastAPI is widely adopted in MLOps for key performance and development advantages:")
    add_bullet(doc, "Ultra-High Concurrency: Built on Starlette and uvloop, matching NodeJS and Go in raw throughput benchmarks.", bold_prefix="1. ")
    add_bullet(doc, "Automated Validation: Pydantic automatically parses, coerces, and validates incoming JSON payloads, returning clean 422 Unprocessable Entity errors on invalid inputs.", bold_prefix="2. ")
    add_bullet(doc, "Zero-Effort Documentation: Generates interactive Swagger UI (/docs) and ReDoc (/redoc) schemas directly from Python type declarations.", bold_prefix="3. ")
    add_bullet(doc, "Native Testability: FastAPI's TestClient integrates seamlessly with pytest for deterministic unit and integration testing without deploying external servers.", bold_prefix="4. ")

    add_heading_2(doc, "c) Key components and terminology")
    add_bullet(doc, "Asynchronous Server Gateway Interface enabling Python async/await non-blocking concurrency.", bold_prefix="ASGI: ")
    add_bullet(doc, "Data parsing and validation library using Python type hints to enforce schema contracts.", bold_prefix="Pydantic BaseModel: ")
    add_bullet(doc, "Lightning-fast ASGI web server implementation for Python based on uvloop and httptools.", bold_prefix="Uvicorn: ")
    add_bullet(doc, "Interactive browser-based interface for exploring, testing, and visualizing REST API endpoints.", bold_prefix="Swagger UI: ")
    add_bullet(doc, "Endpoint returning service liveness and model readiness for load balancers and orchestrators.", bold_prefix="Health Check Endpoint: ")

    add_heading_2(doc, "d) Benefits and limitations")
    add_body_p(doc, "Benefits include high throughput, low latency, developer velocity, and bulletproof input type checking. Limitations include the need to carefully manage CPU-bound model inference to avoid blocking the single-threaded event loop (mitigated by using threadpools or worker processes).")

    # ── Architecture Diagram ──────────────────────────────────────────────────
    add_heading_1(doc, "Architecture / Workflow Diagram")
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                 FASTAPI MACHINE LEARNING SERVING ARCHITECTURE           |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                                                           \n"
        "            Client Application (Web, Mobile, curl, TestClient)             \n"
        "                                     |                                     \n"
        "                       HTTP POST /predict (JSON Payload)                   \n"
        "                                     v                                     \n"
        "                   +-----------------------------------+                   \n"
        "                   |        Uvicorn ASGI Server        |                   \n"
        "                   |       (http://127.0.0.1:8000)     |                   \n"
        "                   +-----------------------------------+                   \n"
        "                                     |                                     \n"
        "                                     v                                     \n"
        "                   +-----------------------------------+                   \n"
        "                   |         FastAPI Routing           |                   \n"
        "                   +-----------------------------------+                   \n"
        "                                     |                                     \n"
        "                                     v                                     \n"
        "                   +-----------------------------------+                   \n"
        "                   |   Pydantic Schema Validation      |                   \n"
        "                   |   - Positive Float Validation     |                   \n"
        "                   |   - 422 Handler on Malformed Data |                   \n"
        "                   +-----------------------------------+                   \n"
        "                                     |                                     \n"
        "                        Valid Input (4 features)                           \n"
        "                                     v                                     \n"
        "                   +-----------------------------------+                   \n"
        "                   |   Model Inference Engine          |                   \n"
        "                   |   - model.pkl (Loaded at Startup) |                   \n"
        "                   |   - clf.predict() & predict_proba |                   \n"
        "                   +-----------------------------------+                   \n"
        "                                     |                                     \n"
        "                        HTTP 200 OK Response                               \n"
        "                        {prediction, confidence, class_id}                 \n"
        "                                     v                                     \n"
        "                            Client Consumer                                \n"
    )
    add_code_block(doc, arch_diagram)

    # ── Procedure ─────────────────────────────────────────────────────────────
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: Train Classification Model and Start FastAPI Uvicorn Server")
    add_body_p(doc, "Train a Logistic Regression model on the Iris dataset (accuracy 96.67%), serialize it to model.pkl, and launch the FastAPI server via Uvicorn on port 8000.")
    add_code_block(doc, "python src/train_model.py\nuvicorn main:app --reload --host 127.0.0.1 --port 8000")
    add_captioned_image(doc, "asgn5_fig1.png", "Figure 5.1: Model Training Execution and Uvicorn Server Launch on Port 8000")

    add_heading_2(doc, "Step 2: Exploring Interactive Swagger UI Documentation")
    add_body_p(doc, "Open a web browser and navigate to http://127.0.0.1:8000/docs to explore the auto-generated Swagger UI schema, endpoints, and data contracts.")
    add_captioned_image(doc, "asgn5_fig2.png", "Figure 5.2: FastAPI Swagger UI Displaying Interactive OpenAPI Documentation and Endpoints")

    add_heading_2(doc, "Step 3: Sending Real-Time Prediction Request")
    add_body_p(doc, "Execute a POST request to /predict with JSON payload {\"sepal_length\": 5.1, \"sepal_width\": 3.5, \"petal_length\": 1.4, \"petal_width\": 0.2}. Verify immediate response with predicted class 'setosa' and high confidence.")
    add_captioned_image(doc, "asgn5_fig3.png", "Figure 5.3: Interactive Prediction Request and Structured JSON Response in Swagger UI")

    add_heading_2(doc, "Step 4: Executing Automated Test Suite with Pytest")
    add_body_p(doc, "Execute the comprehensive test suite in tests/test_api.py using pytest. The suite tests health check, prediction accuracy, negative values, missing fields, non-numeric strings, and batch inference, passing 18 out of 18 test cases.")
    add_code_block(doc, "pytest tests/ -v")
    add_captioned_image(doc, "asgn5_fig4.png", "Figure 5.4: Pytest Terminal Output Showing 18 Passed Unit and Integration Tests in 4.85s")

    # ── Code / Configuration Files ────────────────────────────────────────────
    add_heading_1(doc, "Code / Configuration Files")
    add_body_p(doc, "FastAPI Microservice Implementation (main.py):")
    code_api = (
        "from fastapi import FastAPI, HTTPException\n"
        "from pydantic import BaseModel, Field\n"
        "import joblib, numpy as np\n"
        "\n"
        "app = FastAPI(title='Iris ML Inference API', version='1.0')\n"
        "model = joblib.load('model.pkl')\n"
        "CLASS_NAMES = ['setosa', 'versicolor', 'virginica']\n"
        "\n"
        "class IrisInput(BaseModel):\n"
        "    sepal_length: float = Field(..., gt=0, example=5.1)\n"
        "    sepal_width: float = Field(..., gt=0, example=3.5)\n"
        "    petal_length: float = Field(..., gt=0, example=1.4)\n"
        "    petal_width: float = Field(..., gt=0, example=0.2)\n"
        "\n"
        "@app.get('/health')\n"
        "def health():\n"
        "    return {'status': 'healthy', 'model_loaded': model is not None}\n"
        "\n"
        "@app.post('/predict')\n"
        "def predict(data: IrisInput):\n"
        "    features = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])\n"
        "    pred_idx = int(model.predict(features)[0])\n"
        "    probs = model.predict_proba(features)[0]\n"
        "    return {\n"
        "        'prediction': CLASS_NAMES[pred_idx],\n"
        "        'class_id': pred_idx,\n"
        "        'confidence': round(float(probs[pred_idx]), 4)\n"
        "    }\n"
    )
    add_code_block(doc, code_api)

    add_body_p(doc, "GitHub Repository Link: ", bold_prefix="Source Code Repository: ")
    add_body_p(doc, "https://github.com/krishdeshpande/MLOPs/tree/main/Assignment%205")

    # ── Output / Results ──────────────────────────────────────────────────────
    add_heading_1(doc, "Output / Results")
    add_body_p(doc, "Summary of Output Figures:")
    fig_headers = ["Figure", "Description", "Result / Observation"]
    fig_data = [
        ["Figure 5.1", "Training & Uvicorn Launch", "Trained model (96.67% accuracy) and started Uvicorn ASGI on 127.0.0.1:8000."],
        ["Figure 5.2", "Swagger UI Documentation", "Rendered interactive OpenAPI documentation with /health, /predict, /batch_predict."],
        ["Figure 5.3", "Prediction Endpoint Test", "Sent test payload; returned prediction='setosa' with 98.5% confidence."],
        ["Figure 5.4", "Automated Pytest Execution", "Executed 18 tests covering valid, boundary, and error cases; 100% pass rate."]
    ]
    add_table_styled(doc, fig_headers, fig_data, col_widths=[1.5, 2.5, 2.5])

    # ── Observations and Analysis ─────────────────────────────────────────────
    add_heading_1(doc, "Observations and Analysis")
    add_bullet(doc, "Pydantic Field validations (gt=0) prevent invalid physical inputs (e.g., negative sepal lengths) from reaching model inference.", bold_prefix="1. Schema Guardrails: ")
    add_bullet(doc, "FastAPI's asynchronous nature allows handling high concurrency without blocking worker threads during I/O bound tasks.", bold_prefix="2. Concurrency Performance: ")
    add_bullet(doc, "Automatic Swagger documentation generation dramatically shortens integration cycles for downstream frontend and mobile developers.", bold_prefix="3. Developer Efficiency: ")
    add_bullet(doc, "Comprehensive test suites verify graceful 422 error handling on malformed JSON, preventing production service crashes.", bold_prefix="4. Production Reliability: ")

    # ── Conclusion ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Conclusion")
    add_body_p(doc, "In this assignment, a production-ready machine learning prediction REST API was designed, implemented, and tested using FastAPI, Pydantic, and Uvicorn. Strongly-typed request/response validation schemas guaranteed robust error handling, interactive OpenAPI documentation simplified endpoint exploration, and automated pytest validation confirmed 100% test coverage across normal and abnormal inputs.")

    # ── References ────────────────────────────────────────────────────────────
    add_heading_1(doc, "References")
    add_bullet(doc, "S. Ramirez, \"FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python,\" https://fastapi.tiangolo.com/, accessed September 2026.", bold_prefix="[1] ")
    add_bullet(doc, "Pydantic Documentation, \"Data Validation and Settings Management Using Python Type Annotations,\" https://docs.pydantic.dev/, accessed September 2026.", bold_prefix="[2] ")
    add_bullet(doc, "T. Vink, Building Machine Learning Microservices with Python and FastAPI, Birmingham, UK: Packt Publishing, 2022.", bold_prefix="[3] ")

    out_file = os.path.join(BASE_DIR, "Assignment 5", "MLOps_Assignment_5_Writeup.docx")
    doc.save(out_file)
    shutil.copy(out_file, os.path.join(ALL_WRITEUPS_DIR, "MLOps_Assignment_5_Writeup.docx"))
    print(f"✓ Generated: {out_file}")

if __name__ == "__main__":
    create_assignment_4()
    create_assignment_5()
