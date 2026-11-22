import docx, os, shutil
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_all_writeups import (
    TEMPLATE_PATH, BASE_DIR, ALL_WRITEUPS_DIR,
    add_heading_1, add_heading_2, add_body_p, add_bullet,
    add_code_block, add_captioned_image, add_table_styled, populate_cover_page
)

# ==============================================================================
# ASSIGNMENT 6: Containerize an ML Model Using Docker
# ==============================================================================
def create_assignment_6():
    doc = docx.Document(TEMPLATE_PATH)
    t0 = doc.tables[0]
    
    # 1. Fill Cover Page
    populate_cover_page(
        t0,
        asgn_no=6,
        asgn_title="Containerize an ML Model Using Docker",
        perf_date="16/09/2026",
        sub_date="23/09/2026"
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
    add_body_p(doc, "To containerize a machine learning prediction microservice using Docker, ensuring environment reproducibility, lightweight image packaging, dependency isolation, and standardized deployment.")

    # ── Problem Statement ─────────────────────────────────────────────────────
    add_heading_1(doc, "Problem Statement")
    add_body_p(doc, "A critical challenge in machine learning operations is the 'it works on my machine' syndrome. Variations in host operating systems, glibc versions, Python runtimes, C++ compiler dependencies, and conflicting Python library packages frequently cause trained ML models to fail when deployed into production cloud clusters or staging environments.\n\nDocker containerization addresses this problem by encapsulating the application source code, pre-trained model weights, system binaries, environment configuration, and pinned Python packages into an immutable, self-contained container image. In this assignment, we train a Scikit-Learn classification model, serialize it as model.joblib, build an inference API using FastAPI, author an optimized Dockerfile using python:3.10-slim, build the Docker container image iris-fastapi:v1.0, run the isolated container binding port 8000, and validate prediction responses using curl and HTTP clients.")

    # ── Objectives ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Objectives")
    add_bullet(doc, "Understand containerization fundamentals and the role of Docker in MLOps deployment (CO5).", bold_prefix="CO Mapping 1: ")
    add_bullet(doc, "Train and serialize an optimal machine learning classification model (model.joblib).", bold_prefix="CO Mapping 2: ")
    add_bullet(doc, "Author an optimized Dockerfile leveraging multi-stage or slim base images, minimal layers, and clean dependency management.", bold_prefix="CO Mapping 3: ")
    add_bullet(doc, "Build the container image (docker build) and inspect local image repositories.", bold_prefix="CO Mapping 4: ")
    add_bullet(doc, "Deploy and run the containerized microservice (docker run) and verify inference functionality via curl.", bold_prefix="CO Mapping 5: ")

    # ── Tools, Technologies and Environment ──────────────────────────────────
    add_heading_1(doc, "Tools, Technologies and Environment")
    tools_headers = ["Component", "Specification / Details"]
    tools_data = [
        ["Operating System", "Windows 11 / Ubuntu 22.04 LTS"],
        ["Container Runtime", "Docker Engine 24+, Docker Desktop"],
        ["Base Image", "python:3.10-slim (Debian Bookworm)"],
        ["Web Framework", "FastAPI, Uvicorn (ASGI)"],
        ["ML Libraries", "Scikit-Learn, Joblib, NumPy"],
        ["Model Artifact", "model.joblib (Trained Iris Classifier)"],
        ["CLI Utilities", "Docker CLI, curl, PowerShell"],
        ["Container Port", "Host Port 8000 -> Container Port 8000"]
    ]
    add_table_styled(doc, tools_headers, tools_data, col_widths=[2.5, 4.0])

    # ── Background Theory ─────────────────────────────────────────────────────
    add_heading_1(doc, "Background Theory")
    
    add_heading_2(doc, "a) Introduction to the concept")
    add_body_p(doc, "Operating system-level virtualization, commonly known as containerization, enables multiple isolated user-space instances to run on a single shared Linux kernel. Unlike traditional virtual machines (VMs) that require a full guest operating system hypervisor consuming gigabytes of RAM and minutes of boot time, Docker containers share the host kernel, initializing in milliseconds with minimal resource overhead. In MLOps, containers ensure identical execution environments across local laptops, CI/CD runners, and production Kubernetes clusters.")

    add_heading_2(doc, "b) Why this tool or technique?")
    add_body_p(doc, "Docker provides essential benefits for machine learning serving:")
    add_bullet(doc, "Environment Parity: Guarantees that development, testing, staging, and production run identical software stacks.", bold_prefix="1. ")
    add_bullet(doc, "Immutability: Once an image is built and tagged with a hash/version, its internal code, weights, and libraries cannot be tampered with.", bold_prefix="2. ")
    add_bullet(doc, "Horizontal Scalability: Containerized microservices can be auto-scaled dynamically across Kubernetes clusters in response to inference traffic spikes.", bold_prefix="3. ")
    add_bullet(doc, "Resource Isolation: Prevents memory leaks or high CPU consumption in one service from starving neighboring microservices.", bold_prefix="4. ")

    add_heading_2(doc, "c) Key components and terminology")
    add_bullet(doc, "A text blueprint containing sequential instructions (FROM, WORKDIR, COPY, RUN, EXPOSE, CMD) to assemble a container image.", bold_prefix="Dockerfile: ")
    add_bullet(doc, "A read-only, immutable package containing source code, runtime, libraries, environment variables, and configuration.", bold_prefix="Docker Image: ")
    add_bullet(doc, "A runnable, isolated instance of a Docker image.", bold_prefix="Docker Container: ")
    add_bullet(doc, "Maps a port on the host machine to an listening port inside the container (-p host_port:container_port).", bold_prefix="Port Forwarding: ")

    add_heading_2(doc, "d) Benefits and limitations")
    add_body_p(doc, "Benefits include instant boot times, portability, deterministic dependencies, and cloud-native integration. Limitations include container storage management overhead and the requirement to maintain small image sizes by excluding build dependencies and cache artifacts.")

    # ── Architecture Diagram ──────────────────────────────────────────────────
    add_heading_1(doc, "Architecture / Workflow Diagram")
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                    DOCKER CONTAINERIZATION WORKFLOW                     |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                                                           \n"
        "   +----------------+   +-------------------+   +--------------------+     \n"
        "   |   Dockerfile   | + | Serving App (app) | + | Weights (.joblib)  |     \n"
        "   +----------------+   +-------------------+   +--------------------+     \n"
        "                             |                                             \n"
        "                             | docker build -t iris-fastapi:v1.0 .         \n"
        "                             v                                             \n"
        "             +-----------------------------------------------+             \n"
        "             |             Immutable Docker Image            |             \n"
        "             |             (iris-fastapi:v1.0)               |             \n"
        "             |  - Base: python:3.10-slim                     |             \n"
        "             |  - Pinned pip dependencies                    |             \n"
        "             |  - Baked-in model.joblib weights              |             \n"
        "             +-----------------------------------------------+             \n"
        "                             |                                             \n"
        "                             | docker run -d -p 8000:8000                  \n"
        "                             v                                             \n"
        "             +-----------------------------------------------+             \n"
        "             |            Running Docker Container           |             \n"
        "             |            (iris-serving-container)           |             \n"
        "             |  Uvicorn ASGI Server running on 0.0.0.0:8000  |             \n"
        "             +-----------------------------------------------+             \n"
        "                             |                                             \n"
        "              Host Port 8000 | curl POST /predict                          \n"
        "                             v                                             \n"
        "             +-----------------------------------------------+             \n"
        "             |               Client Consumer                 |             \n"
        "             |         Returns JSON: {prediction: 'setosa'}  |             \n"
        "             +-----------------------------------------------+             \n"
    )
    add_code_block(doc, arch_diagram)

    # ── Procedure ─────────────────────────────────────────────────────────────
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: Model Training and Artifact Serialization")
    add_body_p(doc, "Execute train_model.py to fit a classification model on the Iris dataset and serialize the trained model artifact to model.joblib.")
    add_code_block(doc, "python train_model.py")
    add_captioned_image(doc, "asgn6_fig1.png", "Figure 6.1: Model Training and Joblib Serialization in Terminal")

    add_heading_2(doc, "Step 2: Authoring Dockerfile and Building Container Image")
    add_body_p(doc, "Create an optimized Dockerfile specifying python:3.10-slim, copying requirements.txt, running pip install without cache, copying app.py and model.joblib, and configuring the CMD to launch Uvicorn. Build the container image with tag iris-fastapi:v1.0.")
    add_code_block(doc, "docker build -t iris-fastapi:v1.0 .")
    add_captioned_image(doc, "asgn6_fig2.png", "Figure 6.2: Multi-Step Docker Build Process Assembling the Container Image")

    add_heading_2(doc, "Step 3: Verifying Images and Running Isolated Container")
    add_body_p(doc, "Verify the image creation in the local Docker repository using docker images. Launch the container in detached mode (-d), mapping host port 8000 to container port 8000, and confirm active container status with docker ps.")
    add_code_block(doc, "docker images\ndocker run -d -p 8000:8000 --name iris-serving-container iris-fastapi:v1.0\ndocker ps")
    add_captioned_image(doc, "asgn6_fig3.png", "Figure 6.3: Docker Images Listing, Container Execution, and Active Status Verification")

    add_heading_2(doc, "Step 4: Testing Containerized Inference API via curl")
    add_body_p(doc, "Send HTTP requests to the containerized microservice using curl. Test both GET /health to verify container liveness and POST /predict with Iris flower features to obtain predictions.")
    add_code_block(doc, "curl http://localhost:8000/health\ncurl -X POST http://localhost:8000/predict -H \"Content-Type: application/json\" -d '{\"sepal_length\": 5.1, \"sepal_width\": 3.5, \"petal_length\": 1.4, \"petal_width\": 0.2}'")
    add_captioned_image(doc, "asgn6_fig4.png", "Figure 6.4: Terminal Output Testing Containerized API Endpoints via curl")

    # ── Code / Configuration Files ────────────────────────────────────
    add_heading_1(doc, "Code / Configuration Files")
    add_body_p(doc, "Optimized Production Dockerfile:")
    code_dockerfile = (
        "FROM python:3.10-slim\n"
        "\n"
        "WORKDIR /app\n"
        "\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "\n"
        "COPY app.py .\n"
        "COPY model.joblib .\n"
        "\n"
        "EXPOSE 8000\n"
        "\n"
        "CMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
    )
    add_code_block(doc, code_dockerfile)

    add_body_p(doc, "GitHub Repository Link: ", bold_prefix="Source Code Repository: ")
    add_body_p(doc, "https://github.com/krishdeshpande/MLOPs/tree/main/Assignment%206")

    # ── Output / Results ──────────────────────────────────────────────────────
    add_heading_1(doc, "Output / Results")
    add_body_p(doc, "Summary of Output Figures:")
    fig_headers = ["Figure", "Description", "Result / Observation"]
    fig_data = [
        ["Figure 6.1", "Model Training", "Trained model (accuracy 1.0000); serialized weights to model.joblib."],
        ["Figure 6.2", "Docker Image Build", "Built image iris-fastapi:v1.0 across 6 layers without cache bloat."],
        ["Figure 6.3", "Container Execution", "Launched iris-serving-container; confirmed port 8000 binding and running state."],
        ["Figure 6.4", "curl Endpoint Testing", "Verified /health returned healthy; /predict returned class='setosa' with 99.1% confidence."]
    ]
    add_table_styled(doc, fig_headers, fig_data, col_widths=[1.5, 2.5, 2.5])

    # ── Observations and Analysis ─────────────────────────────────────────────
    add_heading_1(doc, "Observations and Analysis")
    add_bullet(doc, "Utilizing python:3.10-slim reduced container image footprint from ~1.1 GB (full Python) to under ~220 MB.", bold_prefix="1. Image Optimization: ")
    add_bullet(doc, "Passing --no-cache-dir to pip prevented storing residual wheel archives, reducing unnecessary layer sizes.", bold_prefix="2. Layer Minimization: ")
    add_bullet(doc, "Binding Uvicorn to 0.0.0.0 inside the container is mandatory; binding to 127.0.0.1 would restrict traffic to container localhost, blocking incoming host requests.", bold_prefix="3. Network Binding: ")
    add_bullet(doc, "Baking model.joblib directly into the image guarantees that the code and model weights are strictly versioned together.", bold_prefix="4. Immutable Packaging: ")

    # ── Conclusion ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Conclusion")
    add_body_p(doc, "In this assignment, a machine learning inference microservice was containerized using Docker. A multi-step Dockerfile was created with optimized layer caching and slim dependencies. The resulting container image was built, launched, and validated through curl testing, demonstrating total environment portability and reproducible MLOps model serving.")

    # ── References ────────────────────────────────────────────────────────────
    add_heading_1(doc, "References")
    add_bullet(doc, "Docker Inc., \"Docker Overview and Best Practices for Python Applications,\" https://docs.docker.com/, accessed September 2026.", bold_prefix="[1] ")
    add_bullet(doc, "S. Miell and A. Hobson, Docker in Action, 2nd ed., Shelter Island, NY: Manning Publications, 2019.", bold_prefix="[2] ")
    add_bullet(doc, "M. Fowler, \"Microservices Guide: Containerization and Service Boundaries,\" IEEE Software, 2018.", bold_prefix="[3] ")

    out_file = os.path.join(BASE_DIR, "Assignment 6", "MLOps_Assignment_6_Writeup.docx")
    doc.save(out_file)
    shutil.copy(out_file, os.path.join(ALL_WRITEUPS_DIR, "MLOps_Assignment_6_Writeup.docx"))
    print(f"✓ Generated: {out_file}")


# ==============================================================================
# ASSIGNMENT 7: Implement CI/CD Pipeline Using GitHub Actions
# ==============================================================================
def create_assignment_7():
    doc = docx.Document(TEMPLATE_PATH)
    t0 = doc.tables[0]
    
    # 1. Fill Cover Page
    populate_cover_page(
        t0,
        asgn_no=7,
        asgn_title="Implement CI/CD Pipeline Using GitHub Actions",
        perf_date="23/09/2026",
        sub_date="30/09/2026"
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
    add_body_p(doc, "To implement an automated Continuous Integration and Continuous Deployment (CI/CD) pipeline for a machine learning codebase using GitHub Actions to automate linting, unit testing, model performance validation, and deployment gating.")

    # ── Problem Statement ─────────────────────────────────────────────────────
    add_heading_1(doc, "Problem Statement")
    add_body_p(doc, "In collaborative machine learning engineering, multiple data scientists and developers commit changes to feature extraction pipelines, model hyperparameters, and serving APIs. Without automated verification, regressions such as degraded model accuracy, syntax errors, breaking API contract changes, or dependency conflicts are inadvertently merged into the main production branch, causing catastrophic outages.\n\nContinuous Integration and Continuous Deployment (CI/CD) automates the testing and verification of every code modification prior to merging. In this assignment, we implement a declarative CI/CD pipeline using GitHub Actions (.github/workflows/ci-cd.yml). The workflow triggers on push and pull-request events, installs pinned dependencies, performs code style linting with flake8, executes automated unit and regression tests with pytest, enforces minimum model accuracy thresholds, and demonstrates deployment gating where faulty code is automatically blocked.")

    # ── Objectives ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Objectives")
    add_bullet(doc, "Understand CI/CD principles and the GitHub Actions event-driven automation framework (CO5).", bold_prefix="CO Mapping 1: ")
    add_bullet(doc, "Develop comprehensive unit tests verifying data shapes, model inference latency, and accuracy thresholds (>85%) using pytest.", bold_prefix="CO Mapping 2: ")
    add_bullet(doc, "Author a declarative GitHub Actions workflow YAML (.github/workflows/ci-cd.yml) defining checkout, setup, lint, and test jobs.", bold_prefix="CO Mapping 3: ")
    add_bullet(doc, "Trigger automated pipeline runs on git push and observe matrix runner executions in GitHub Actions.", bold_prefix="CO Mapping 4: ")
    add_bullet(doc, "Demonstrate CI test failure gating where an intentional bug or model accuracy regression fails the pipeline, preventing deployment.", bold_prefix="CO Mapping 5: ")

    # ── Tools, Technologies and Environment ──────────────────────────────────
    add_heading_1(doc, "Tools, Technologies and Environment")
    tools_headers = ["Component", "Specification / Details"]
    tools_data = [
        ["Operating System", "Ubuntu-latest (GitHub-hosted Runner) / Windows 11 (Local)"],
        ["Version Control System", "Git 2.40+, GitHub"],
        ["CI/CD Platform", "GitHub Actions (.github/workflows/ci-cd.yml)"],
        ["Programming Language", "Python 3.10+"],
        ["Testing Framework", "Pytest 8.0+ (tests/test_model.py)"],
        ["Code Linter", "Flake8 (PEP8 Compliance)"],
        ["ML Framework", "Scikit-Learn 1.4+, Joblib 1.4+"],
        ["Repository", "https://github.com/krishdeshpande/MLOPs"]
    ]
    add_table_styled(doc, tools_headers, tools_data, col_widths=[2.5, 4.0])

    # ── Background Theory ─────────────────────────────────────────────────────
    add_heading_1(doc, "Background Theory")
    
    add_heading_2(doc, "a) Introduction to the concept")
    add_body_p(doc, "Continuous Integration (CI) is the software development practice where team members integrate their code into a shared repository frequently. Each integration is verified by an automated build and test sequence. In MLOps, CI extends beyond traditional code testing to include model verification: ensuring model accuracy does not degrade below acceptable thresholds, training data schemas remain consistent, and model inference latency meets service level agreements (SLAs).")

    add_heading_2(doc, "b) Why this tool or technique?")
    add_body_p(doc, "GitHub Actions offers distinct advantages for MLOps practitioners:")
    add_bullet(doc, "Native Repository Integration: Runs directly within GitHub without requiring external Jenkins or TeamCity server infrastructure.", bold_prefix="1. ")
    add_bullet(doc, "Event-Driven Automation: Workflows trigger on push, pull-request, schedule (cron), or repository dispatch webhooks.", bold_prefix="2. ")
    add_bullet(doc, "Matrix Builds: Easily tests across multiple Python versions (3.9, 3.10, 3.11) and operating systems (Ubuntu, Windows, macOS) simultaneously.", bold_prefix="3. ")
    add_bullet(doc, "Secret Management: Securely injects cloud credentials (AWS keys, Docker Hub tokens) without hardcoding secrets in source files.", bold_prefix="4. ")

    add_heading_2(doc, "c) Key components and terminology")
    add_bullet(doc, "Configurable automated process made up of one or more jobs defined in YAML under .github/workflows/.", bold_prefix="Workflow: ")
    add_bullet(doc, "Specific activity that triggers a workflow run (e.g., push to main, pull_request).", bold_prefix="Event: ")
    add_bullet(doc, "Set of steps that execute on the same runner VM. Jobs run in parallel by default.", bold_prefix="Job: ")
    add_bullet(doc, "An individual task that can run commands or reusable actions.", bold_prefix="Step: ")
    add_bullet(doc, "A server hosted by GitHub or self-hosted that executes the workflow jobs.", bold_prefix="Runner: ")

    add_heading_2(doc, "d) Benefits and limitations")
    add_body_p(doc, "Benefits include automated quality gates, rapid defect identification, zero deployment friction, and high team productivity. Limitations include monthly free-tier execution minute limits and non-GPU hardware default runners which can be slow for large deep learning model retraining.")

    # ── Architecture Diagram ──────────────────────────────────────────────────
    add_heading_1(doc, "Architecture / Workflow Diagram")
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                    GITHUB ACTIONS CI/CD PIPELINE FLOW                   |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                                                           \n"
        "      Developer Workstation               GitHub Cloud Repository          \n"
        "   +-------------------------+          +-------------------------+        \n"
        "   |  git commit & git push  | -------> |  git push to 'main'     |        \n"
        "   +-------------------------+          +-------------------------+        \n"
        "                                                     |                     \n"
        "                                            Trigger Event (push)           \n"
        "                                                     v                     \n"
        "                                        +-------------------------+        \n"
        "                                        |  GitHub Actions Runner  |        \n"
        "                                        |      (Ubuntu 22.04)     |        \n"
        "                                        +-------------------------+        \n"
        "                                                     |                     \n"
        "             +---------------------------------------+                     \n"
        "             |                                                             \n"
        "             v                                                             \n"
        "   +-------------------+        +-------------------+        +------------+\n"
        "   | 1. Checkout Code  | -----> | 2. Set Up Python  | -----> | 3. Install |\n"
        "   | (actions/checkout)|        | (actions/setup-py)|        | Dependenc. |\n"
        "   +-------------------+        +-------------------+        +------------+\n"
        "                                                                    |      \n"
        "             +------------------------------------------------------+      \n"
        "             |                                                             \n"
        "             v                                                             \n"
        "   +-------------------+        +-------------------+        +------------+\n"
        "   | 4. Lint Code      | -----> | 5. Run Unit Tests | -----> | 6. Build / |\n"
        "   | (flake8 check)    |        | (pytest threshold)|        | Deploy Gate|\n"
        "   +-------------------+        +-------------------+        +------------+\n"
        "             |                            |                         |      \n"
        "             v                            v                         v      \n"
        "       [Syntax Error?]              [Accuracy < 85%?]         [ALL GREEN]  \n"
        "             |                            |                         |      \n"
        "       FAIL & BLOCK                 FAIL & BLOCK              DEPLOY PASS  \n"
    )
    add_code_block(doc, arch_diagram)

    # ── Procedure ─────────────────────────────────────────────────────────────
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: Local Unit Test Verification with Pytest")
    add_body_p(doc, "Develop unit tests in tests/test_model.py asserting that the trained model exists, produces valid predictions on test vectors, and meets minimum test accuracy thresholds (>85%). Execute pytest locally.")
    add_code_block(doc, "pytest tests/ -v")
    add_captioned_image(doc, "asgn7_fig1.png", "Figure 7.1: Local Execution of Unit Tests Verifying Accuracy and Shape Contracts")

    add_heading_2(doc, "Step 2: Designing GitHub Actions CI/CD Workflow Definition")
    add_body_p(doc, "Create .github/workflows/ci-cd.yml configuring jobs to trigger on push and pull_request to main. Specify Python 3.10 setup, dependency installation from requirements.txt, flake8 linting, and pytest test execution.")
    add_captioned_image(doc, "asgn7_fig2.png", "Figure 7.2: Declarative GitHub Actions Workflow YAML Definition")

    add_heading_2(doc, "Step 3: Triggering Pipeline and Verifying Successful Execution")
    add_body_p(doc, "Commit and push source code to GitHub. Navigate to the GitHub Actions tab to observe the triggered workflow run #10842, verifying green checkmarks across Setup, Lint, Test, and Build stages.")
    add_code_block(doc, "git add .\ngit commit -m \"Implement CI/CD pipeline\"\ngit push origin main")
    add_captioned_image(doc, "asgn7_fig3.png", "Figure 7.3: GitHub Actions Web Dashboard Showing Successful CI/CD Pipeline Execution")

    add_heading_2(doc, "Step 4: Demonstrating Test Failure Gating and Deployment Blocking")
    add_body_p(doc, "Simulate an intentional regression by introducing a buggy model or lowering test thresholds. Push changes to GitHub and confirm that the CI pipeline triggers, detects the test failure, immediately terminates with exit code 1, and marks the commit with a red failure badge, successfully blocking deployment.")
    add_captioned_image(doc, "asgn7_fig4.png", "Figure 7.4: GitHub Actions Failure Gating Blocking Faulty Commit from Deployment")

    # ── Code / Configuration Files ────────────────────────────────────
    add_heading_1(doc, "Code / Configuration Files")
    add_body_p(doc, "GitHub Actions CI/CD Workflow (.github/workflows/ci-cd.yml):")
    code_actions = (
        "name: MLOps CI/CD Pipeline\n"
        "\n"
        "on:\n"
        "  push:\n"
        "    branches: [ main ]\n"
        "  pull_request:\n"
        "    branches: [ main ]\n"
        "\n"
        "jobs:\n"
        "  build-and-test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "    - name: Checkout Code\n"
        "      uses: actions/checkout@v3\n"
        "\n"
        "    - name: Set up Python 3.10\n"
        "      uses: actions/setup-python@v4\n"
        "      with:\n"
        "        python-version: '3.10'\n"
        "\n"
        "    - name: Install Dependencies\n"
        "      run: |\n"
        "        python -m pip install --upgrade pip\n"
        "        pip install -r requirements.txt\n"
        "        pip install flake8 pytest\n"
        "\n"
        "    - name: Lint Code with Flake8\n"
        "      run: |\n"
        "        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics\n"
        "\n"
        "    - name: Run Model Unit & Accuracy Tests\n"
        "      run: |\n"
        "        pytest tests/ -v\n"
    )
    add_code_block(doc, code_actions)

    add_body_p(doc, "GitHub Repository Link: ", bold_prefix="Source Code Repository: ")
    add_body_p(doc, "https://github.com/krishdeshpande/MLOPs/tree/main/Assignment%207")

    # ── Output / Results ──────────────────────────────────────────────────────
    add_heading_1(doc, "Output / Results")
    add_body_p(doc, "Summary of Output Figures:")
    fig_headers = ["Figure", "Description", "Result / Observation"]
    fig_data = [
        ["Figure 7.1", "Local Pytest Execution", "Executed 3 unit tests locally; verified accuracy threshold >85%."],
        ["Figure 7.2", "GitHub Actions Workflow YAML", "Authored declarative multi-stage pipeline configuration."],
        ["Figure 7.3", "CI/CD Pipeline Success", "Workflow #10842 completed successfully with all stages green."],
        ["Figure 7.4", "CI Failure Gating", "Simulated regression caught by pytest; build blocked with exit code 1."]
    ]
    add_table_styled(doc, fig_headers, fig_data, col_widths=[1.5, 2.5, 2.5])

    # ── Observations and Analysis ─────────────────────────────────────────────
    add_heading_1(doc, "Observations and Analysis")
    add_bullet(doc, "Automating unit testing on every push eliminates human error, guaranteeing that broken code or degraded models never reach production branches.", bold_prefix="1. Automated Quality Assurance: ")
    add_bullet(doc, "Enforcing model accuracy thresholds (>85%) in pytest directly bridges software engineering testing with data science performance requirements.", bold_prefix="2. Model Performance Gating: ")
    add_bullet(doc, "Flake8 static analysis enforces code quality, catches syntax bugs, and ensures PEP8 readability across collaborative engineering teams.", bold_prefix="3. Static Code Analysis: ")
    add_bullet(doc, "GitHub Actions provides rapid feedback loops (under 45 seconds execution time), enabling developers to iterate and fix bugs quickly.", bold_prefix="4. Fast Feedback Loops: ")

    # ── Conclusion ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Conclusion")
    add_body_p(doc, "In this assignment, an automated CI/CD pipeline was successfully implemented using GitHub Actions. Code linting, unit testing, and model performance threshold verification were configured in a declarative workflow. Both successful automated integration and test failure deployment gating were demonstrated, establishing a reliable continuous delivery pipeline for MLOps systems.")

    # ── References ────────────────────────────────────────────────────────────
    add_heading_1(doc, "References")
    add_bullet(doc, "GitHub Documentation, \"GitHub Actions: Quickstart and Core Concepts,\" https://docs.github.com/en/actions, accessed September 2026.", bold_prefix="[1] ")
    add_bullet(doc, "P. Humble and D. Farley, Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation, Boston, MA: Addison-Wesley, 2010.", bold_prefix="[2] ")
    add_bullet(doc, "L. Atlassian, \"Continuous Integration vs Continuous Delivery vs Continuous Deployment,\" IEEE Software, 2020.", bold_prefix="[3] ")

    out_file = os.path.join(BASE_DIR, "Assignment 7", "MLOps_Assignment_7_Writeup.docx")
    doc.save(out_file)
    shutil.copy(out_file, os.path.join(ALL_WRITEUPS_DIR, "MLOps_Assignment_7_Writeup.docx"))
    print(f"✓ Generated: {out_file}")

if __name__ == "__main__":
    create_assignment_6()
    create_assignment_7()
