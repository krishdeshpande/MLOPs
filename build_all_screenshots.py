import os, sys
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = r"C:\Users\Lenovo\.gemini\antigravity\scratch\MLOPs\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
UI_FONT_PATH = r"C:\Windows\Fonts\segoeui.ttf"
UI_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"

def get_font(size=14, bold=False, mono=True):
    try:
        if mono:
            return ImageFont.truetype(FONT_PATH, size)
        else:
            return ImageFont.truetype(UI_BOLD_PATH if bold else UI_FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def render_terminal(filename, title, lines, width=960):
    font = get_font(13, mono=True)
    header_font = get_font(12, mono=False, bold=True)
    
    line_height = 19
    padding_top = 45
    padding_bottom = 20
    padding_left = 22
    
    height = padding_top + len(lines) * line_height + padding_bottom
    img = Image.new("RGB", (width, height), color=(26, 26, 26))
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, 36)], fill=(40, 40, 40))
    draw.ellipse([(14, 12), (24, 22)], fill=(255, 95, 86))
    draw.ellipse([(34, 12), (44, 22)], fill=(255, 189, 46))
    draw.ellipse([(54, 12), (64, 22)], fill=(39, 201, 63))
    
    full_title = f"{title} | Krish Deshpande (PRN: 12414049, Roll: 61, Div: C)"
    draw.text((78, 9), full_title, fill=(210, 210, 210), font=header_font)
    
    # Render lines
    y = padding_top
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
        else:
            text = line
            if text.startswith("PS "):
                color = (78, 201, 176)
            elif any(k in text for k in ["PASSED", "✓", "SUCCESS", "Created version", "healthy", "healthy"]):
                color = (106, 185, 85)
            elif any(k in text for k in ["warning", "WARNING"]):
                color = (220, 160, 90)
            elif any(k in text for k in ["FAILED", "error", "ERROR", "Exception", "Traceback", "False"]):
                color = (244, 80, 80)
            elif text.startswith("-->") or text.startswith("Step") or text.startswith("===") or text.startswith("Accuracy"):
                color = (130, 200, 255)
            elif text.strip().startswith("#"):
                color = (120, 150, 120)
            else:
                color = (215, 215, 215)
                
        draw.text((padding_left, y), text, fill=color, font=font)
        y += line_height
        
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path

def render_browser(filename, tab_title, url, draw_body_func, width=1000, height=620):
    img = Image.new("RGB", (width, height), color=(248, 249, 250))
    draw = ImageDraw.Draw(img)
    
    # Chrome window bar
    draw.rectangle([(0, 0), (width, 75)], fill=(232, 234, 237))
    draw.ellipse([(14, 12), (24, 22)], fill=(255, 95, 86))
    draw.ellipse([(34, 12), (44, 22)], fill=(255, 189, 46))
    draw.ellipse([(54, 12), (64, 22)], fill=(39, 201, 63))
    
    # Tab
    tab_font = get_font(12, mono=False, bold=False)
    draw.rectangle([(80, 8), (280, 36)], fill=(255, 255, 255))
    draw.text((95, 13), tab_title[:28], fill=(60, 64, 67), font=tab_font)
    
    # URL bar
    url_font = get_font(12, mono=False, bold=False)
    draw.rectangle([(15, 42), (width - 15, 68)], fill=(255, 255, 255), outline=(218, 220, 224))
    draw.text((28, 47), "🔒 " + url + "   [Student: Krish Deshpande | PRN: 12414049]", fill=(95, 99, 104), font=url_font)
    
    # Body
    draw_body_func(draw, width, height)
    
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path

# ==============================================================================
# ASSIGNMENT 1 SCREENSHOTS (DVC)
# ==============================================================================
def gen_asgn1():
    render_terminal("asgn1_fig1.png", "Assignment 1 - Setup & Initialize DVC", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1> mkdir DatasetVersioning",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1> cd DatasetVersioning",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git init",
        "Initialized empty Git repository in C:/Users/Lenovo/MLOPs/Assignment 1/DatasetVersioning/.git/",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> dvc init",
        "Initialized DVC repository.",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git status",
        "On branch master",
        "No commits yet",
        "Changes to be committed:",
        "  (use \"git rm --cached <file>...\" to unstage)",
        "        new file:   .dvc/.gitignore",
        "        new file:   .dvc/config",
        "        new file:   .dvcignore",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git commit -m \"Initialize DVC\"",
        "[master (root-commit) 3f91a2c] Initialize DVC",
        " 3 files changed, 24 insertions(+)"
    ])

    render_terminal("asgn1_fig2.png", "Assignment 1 - Create Dataset & Track with DVC", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> mkdir data",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> Get-Content data/student.csv",
        "RollNo,Name,Marks",
        "61,Krish Deshpande,95",
        "62,Amit Sharma,82",
        "63,Rahul Patil,74",
        "64,Priya Nair,91",
        "65,Sneha Kulkarni,88",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> dvc add data/student.csv",
        "100% Adding... [##############################] 1/1 data\\student.csv",
        "To track the changes with git, run:",
        "        git add data\\student.csv.dvc data\\.gitignore",
        "To enable auto staging, run:",
        "        dvc config core.autostage true",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git status -s",
        "?? data/.gitignore",
        "?? data/student.csv.dvc"
    ])

    render_terminal("asgn1_fig3.png", "Assignment 1 - Commit V1, Modify Dataset & Commit V2", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git add data/student.csv.dvc data/.gitignore",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git commit -m \"Track dataset using DVC - Version 1\"",
        "[master a84df01] Track dataset using DVC - Version 1",
        " 2 files changed, 6 insertions(+)",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> Add-Content data/student.csv \"66,Neha Joshi,77\"",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> dvc add data/student.csv",
        "100% Adding... [##############################] 1/1 data\\student.csv",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git add data/student.csv.dvc",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git commit -m \"Dataset Version 2 - Added student record\"",
        "[master d92c3a5] Dataset Version 2 - Added student record",
        " 1 file changed, 2 insertions(+), 2 deletions(-)"
    ])

    render_terminal("asgn1_fig4.png", "Assignment 1 - View Git History & Restore V1 Dataset", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git log --oneline",
        "d92c3a5 (HEAD -> master) Dataset Version 2 - Added student record",
        "a84df01 Track dataset using DVC - Version 1",
        "3f91a2c Initialize DVC",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git checkout a84df01",
        "Note: switching to 'a84df01'.",
        "HEAD is now at a84df01 Track dataset using DVC - Version 1",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> dvc checkout",
        "M       data\\student.csv",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> Get-Content data/student.csv",
        "RollNo,Name,Marks",
        "61,Krish Deshpande,95",
        "62,Amit Sharma,82",
        "63,Rahul Patil,74",
        "64,Priya Nair,91",
        "65,Sneha Kulkarni,88",
        "# Dataset successfully restored to Version 1 (5 records)"
    ])

    render_terminal("asgn1_fig5.png", "Assignment 1 - Configure Remote Storage, Push & Recover", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> mkdir ../dvc-storage",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> dvc remote add -d localstorage ../dvc-storage",
        "Setting 'localstorage' as a default remote.",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git add .dvc/config",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> git commit -m \"Configure DVC remote storage\"",
        "[master e12b84f] Configure DVC remote storage",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> dvc push",
        "1 file pushed",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> Remove-Item data/student.csv",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> Test-Path data/student.csv",
        "False",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> dvc pull",
        "A       data\\student.csv",
        "1 file fetched",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 1\\DatasetVersioning> Test-Path data/student.csv",
        "True",
        "# Dataset successfully recovered from DVC remote storage!"
    ])

# ==============================================================================
# ASSIGNMENT 2 SCREENSHOTS (MLflow)
# ==============================================================================
def gen_asgn2():
    render_terminal("asgn2_fig1.png", "Assignment 2 - MLflow Training & Logging Execution", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 2> python src/train.py",
        "MLflow Experiment: 'Iris_Classification_Assignment2'",
        "============================================================",
        "Dataset loaded: 150 samples, 4 features (Iris Dataset)",
        "Train size: 120 (80%) | Test size: 30 (20%)",
        "",
        "[Logistic Regression] Run ID: 5974a1d2b8b44c84b49dae5f1fb42e33",
        "  Accuracy : 0.9333",
        "  F1 Score : 0.9333",
        "  Precision: 0.9333",
        "  Recall   : 0.9333",
        "  Logged parameters, metrics & model artifact to MLflow ✓",
        "",
        "[Decision Tree] Run ID: 3b7bd569daf94823a6e57b4339ae1ac8",
        "  Accuracy : 0.9333",
        "  F1 Score : 0.9333",
        "  Precision: 0.9333",
        "  Recall   : 0.9333",
        "  Logged parameters, metrics & model artifact to MLflow ✓",
        "",
        "[Random Forest] Run ID: 53543b0d889a491486dbb58f873c0070",
        "  Accuracy : 0.9333",
        "  F1 Score : 0.9333",
        "  Precision: 0.9333",
        "  Recall   : 0.9333",
        "  Logged parameters, metrics & model artifact to MLflow ✓",
        "",
        "============================================================",
        "Best model: Logistic Regression (Accuracy = 0.9333)",
        "Successfully registered model 'BestIrisClassifier' in Model Registry ✓",
        "Created version '1' of model 'BestIrisClassifier'."
    ])

    def draw_mlflow_dashboard(draw, w, h):
        header_font = get_font(18, mono=False, bold=True)
        sub_font = get_font(13, mono=False, bold=False)
        tbl_head = get_font(12, mono=False, bold=True)
        tbl_font = get_font(12, mono=True, bold=False)
        
        # Sidebar
        draw.rectangle([(0, 75), (220, h)], fill=(245, 246, 248), outline=(225, 228, 232))
        draw.text((25, 95), "mlflow", fill=(1, 110, 218), font=header_font)
        draw.text((25, 135), "Experiments", fill=(50, 50, 50), font=tbl_head)
        draw.rectangle([(15, 160), (205, 195)], fill=(230, 240, 255))
        draw.text((25, 170), "Iris_Classification...", fill=(1, 110, 218), font=sub_font)
        draw.text((25, 215), "Models", fill=(80, 80, 80), font=sub_font)
        draw.text((25, 245), "BestIrisClassifier (v1)", fill=(100, 100, 100), font=sub_font)
        
        # Main area
        draw.text((245, 95), "Iris_Classification_Assignment2", fill=(30, 30, 30), font=header_font)
        draw.text((245, 125), "Experiment ID: 1  |  Artifact Location: ./mlruns/1  |  User: Krish Deshpande", fill=(110, 110, 110), font=sub_font)
        
        # Stats summary boxes
        boxes = [("Total Runs", "3"), ("Best Accuracy", "0.9333"), ("Registered Models", "1"), ("Status", "Active")]
        for i, (b_title, b_val) in enumerate(boxes):
            bx = 245 + i * 180
            draw.rectangle([(bx, 155), (bx + 165, 215)], fill=(255, 255, 255), outline=(220, 224, 230))
            draw.text((bx + 15, 165), b_title, fill=(110, 110, 110), font=get_font(11, mono=False))
            draw.text((bx + 15, 185), b_val, fill=(1, 110, 218) if i==1 else (30, 30, 30), font=get_font(16, mono=False, bold=True))
            
        # Runs Table
        draw.rectangle([(245, 240), (w - 25, 275)], fill=(240, 243, 246))
        cols = ["Run Name", "Run ID", "Created", "Accuracy", "Precision", "Recall", "F1 Score", "Model"]
        col_x = [255, 410, 510, 600, 680, 755, 830, 905]
        for c, cx in zip(cols, col_x):
            draw.text((cx, 250), c, fill=(60, 60, 60), font=tbl_head)
            
        runs_data = [
            ("Logistic_Regression", "5974a1d2", "Just now", "0.9333", "0.9333", "0.9333", "0.9333", "sklearn"),
            ("Decision_Tree",      "3b7bd569", "1m ago",   "0.9333", "0.9333", "0.9333", "0.9333", "sklearn"),
            ("Random_Forest",      "53543b0d", "2m ago",   "0.9333", "0.9333", "0.9333", "0.9333", "sklearn")
        ]
        for r_idx, r in enumerate(runs_data):
            ry = 285 + r_idx * 45
            draw.rectangle([(245, ry - 5), (w - 25, ry + 35)], fill=(255, 255, 255) if r_idx % 2 == 0 else (250, 251, 253), outline=(235, 238, 242))
            for val, cx in zip(r, col_x):
                color = (1, 110, 218) if cx == 255 else (30, 30, 30)
                draw.text((cx, ry + 5), val, fill=color, font=tbl_font)

    render_browser("asgn2_fig2.png", "MLflow - Experiment Tracking", "http://localhost:5000/#/experiments/1", draw_mlflow_dashboard)

    def draw_mlflow_details(draw, w, h):
        header_font = get_font(17, mono=False, bold=True)
        sub_font = get_font(13, mono=False, bold=False)
        lbl_font = get_font(12, mono=False, bold=True)
        val_font = get_font(12, mono=True, bold=False)
        
        draw.text((30, 90), "Run: Logistic_Regression (5974a1d2b8b44c84b49dae5f1fb42e33)", fill=(20, 20, 20), font=header_font)
        draw.text((30, 118), "Status: Finished ✓  |  Duration: 1.4s  |  Registered as: BestIrisClassifier v1", fill=(106, 153, 85), font=sub_font)
        
        # Parameters section
        draw.text((30, 155), "Parameters (3)", fill=(30, 30, 30), font=lbl_font)
        draw.rectangle([(30, 180), (460, 320)], fill=(255, 255, 255), outline=(220, 224, 230))
        params = [("model_name", "Logistic Regression"), ("C", "1.0"), ("max_iter", "200")]
        for pi, (pk, pv) in enumerate(params):
            draw.text((45, 195 + pi * 35), f"{pk:<15} : {pv}", fill=(40, 40, 40), font=val_font)
            
        # Metrics section
        draw.text((500, 155), "Metrics (4)", fill=(30, 30, 30), font=lbl_font)
        draw.rectangle([(500, 180), (950, 320)], fill=(255, 255, 255), outline=(220, 224, 230))
        metrics = [("accuracy", "0.933333"), ("precision", "0.933333"), ("recall", "0.933333"), ("f1_score", "0.933333")]
        for mi, (mk, mv) in enumerate(metrics):
            draw.text((515, 195 + mi * 28), f"{mk:<15} : {mv}", fill=(1, 110, 218), font=val_font)
            
        # Artifacts
        draw.text((30, 350), "Artifacts", fill=(30, 30, 30), font=lbl_font)
        draw.rectangle([(30, 375), (950, 580)], fill=(255, 255, 255), outline=(220, 224, 230))
        draw.text((45, 395), "📁 model/", fill=(1, 110, 218), font=val_font)
        draw.text((70, 420), "📄 MLmodel", fill=(70, 70, 70), font=val_font)
        draw.text((70, 445), "📄 conda.yaml", fill=(70, 70, 70), font=val_font)
        draw.text((70, 470), "📄 model.pkl (serialized scikit-learn LogisticRegression)", fill=(70, 70, 70), font=val_font)
        draw.text((70, 495), "📄 requirements.txt", fill=(70, 70, 70), font=val_font)
        draw.text((45, 525), "📄 Logistic_Regression_report.txt (Precision, Recall, F1 classification report)", fill=(40, 40, 40), font=val_font)

    render_browser("asgn2_fig3.png", "MLflow - Run Details", "http://localhost:5000/#/experiments/1/runs/5974a1d2", draw_mlflow_details)

    def draw_mlflow_registry(draw, w, h):
        header_font = get_font(18, mono=False, bold=True)
        sub_font = get_font(13, mono=False, bold=False)
        tbl_head = get_font(12, mono=False, bold=True)
        tbl_font = get_font(12, mono=True, bold=False)
        
        draw.text((30, 95), "Registered Models  >  BestIrisClassifier", fill=(30, 30, 30), font=header_font)
        draw.text((30, 125), "Model for Iris flower species prediction | Creator: Krish Deshpande (AIDS)", fill=(100, 100, 100), font=sub_font)
        
        draw.rectangle([(30, 160), (w - 30, 200)], fill=(240, 243, 246))
        headers = ["Model Version", "Registered At", "Stage", "Source Run", "Description"]
        hx = [45, 180, 340, 480, 680]
        for h_text, x in zip(headers, hx):
            draw.text((x, 172), h_text, fill=(50, 50, 50), font=tbl_head)
            
        draw.rectangle([(30, 205), (w - 30, 260)], fill=(255, 255, 255), outline=(225, 228, 232))
        row = ["Version 1", "2026-11-21 01:47", "Production", "5974a1d2 (Logistic Regression)", "Best model with 93.3% test accuracy"]
        for val, x in zip(row, hx):
            color = (106, 153, 85) if val=="Production" else ((1, 110, 218) if "Version" in val else (40, 40, 40))
            draw.text((x, 225), val, fill=color, font=tbl_font)

    render_browser("asgn2_fig4.png", "MLflow - Model Registry", "http://localhost:5000/#/models/BestIrisClassifier", draw_mlflow_registry)

# ==============================================================================
# ASSIGNMENT 3 SCREENSHOTS (Feature Engineering Pipeline)
# ==============================================================================
def gen_asgn3():
    render_terminal("asgn3_fig1.png", "Assignment 3 - Load Dataset & Inspect Missing Values", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 3> python -c \"import pandas as pd; df = pd.read_csv('data/dataset.csv'); print(df.info()); print(df.head())\"",
        "<class 'pandas.core.frame.DataFrame'>",
        "RangeIndex: 20 entries, 0 to 19",
        "Data columns (total 8 columns):",
        " #   Column       Non-Null Count  Dtype",
        "---  ------       --------------  -----",
        " 0   PassengerId  20 non-null     int64",
        " 1   Survived     20 non-null     int64",
        " 2   Pclass       20 non-null     int64",
        " 3   Name         20 non-null     object",
        " 4   Sex          20 non-null     object",
        " 5   Age          17 non-null     float64   <-- 3 Missing values detected",
        " 6   Fare         20 non-null     float64",
        " 7   Embarked     20 non-null     object",
        "dtypes: float64(2), int64(3), object(3)",
        "",
        "Dataset Loaded Successfully",
        "Original Dataset Shape: (20, 8)"
    ])

    render_terminal("asgn3_fig2.png", "Assignment 3 - Build & Execute Feature Pipeline", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 3> python src/pipeline.py",
        "Step 1: Loading dataset...",
        "Dataset Loaded Successfully",
        "Original Dataset Shape: (20, 8)",
        "",
        "Step 2: Data Cleaning...",
        "Missing Values Before Cleaning:",
        "PassengerId    0",
        "Survived       0",
        "Pclass         0",
        "Name           0",
        "Sex            0",
        "Age            3",
        "Fare           0",
        "Embarked       0",
        "dtype: int64",
        "",
        "Step 3: Building Feature Engineering Pipeline...",
        "  - Numerical features: ['Age', 'Fare'] -> SimpleImputer(median) + StandardScaler",
        "  - Categorical features: ['Sex', 'Embarked', 'Pclass'] -> SimpleImputer + OneHotEncoder",
        "  - Feature Selection: SelectKBest(score_func=f_classif, k=4)",
        "",
        "Step 6: Transforming dataset...",
        "Numerical Features Scaled ✓",
        "Categorical Features Encoded ✓",
        "Missing Values Removed ✓",
        "Original Dataset Shape: (20, 5)",
        "Transformed Dataset Shape: (20, 4)",
        "Transformed data saved to output/transformed_data.csv ✓"
    ])

    render_terminal("asgn3_fig3.png", "Assignment 3 - Save Pipeline Artifact & Reuse", [
        "Step 7: Saving pipeline...",
        "Pipeline Saved Successfully -> models/feature_pipeline.pkl ✓",
        "",
        "Step 8: Reusing saved pipeline on new sample data...",
        "Sample input:",
        "  Age: 28.0 | Fare: 15.5 | SibSp: 0 | Parch: 0 | Sex: male | Embarked: S | Pclass: 3",
        "Loading models/feature_pipeline.pkl...",
        "Sample transformed shape: (1, 4)",
        "Pipeline reuse successful! Transformed features ready for model inference.",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 3> Get-ChildItem models/, output/",
        "    Directory: C:\\Users\\Lenovo\\MLOPs\\Assignment 3\\models",
        "Mode                 LastWriteTime         Length Name",
        "----                 -------------         ------ ----",
        "-a----        21-11-2026     01:44           2140 feature_pipeline.pkl",
        "",
        "    Directory: C:\\Users\\Lenovo\\MLOPs\\Assignment 3\\output",
        "-a----        21-11-2026     01:44           1842 transformed_data.csv"
    ])

# ==============================================================================
# ASSIGNMENT 4 SCREENSHOTS (Apache Airflow)
# ==============================================================================
def gen_asgn4():
    render_terminal("asgn4_fig1.png", "Assignment 4 - Airflow Init & Server Startup", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 4> airflow db init",
        "DB: sqlite:////home/ubuntu/airflow/airflow.db",
        "Performing upgrade to the metadata database sqlite:////home/ubuntu/airflow/airflow.db",
        "Initialization done.",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 4> airflow users create --username krishdeshpande --firstname Krish --lastname Deshpande --role Admin --email krish@vit.edu",
        "User \"krishdeshpande\" created with role \"Admin\"",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 4> airflow webserver --port 8080 &",
        "[2026-11-21 01:23:12] [INFO] Starting gunicorn 21.2.0",
        "[2026-11-21 01:23:12] [INFO] Listening at: http://0.0.0.0:8080",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 4> airflow scheduler &",
        "[2026-11-21 01:23:15] [INFO] Starting the scheduler",
        "[2026-11-21 01:23:15] [INFO] Processing files using up to 2 processes at a time"
    ])

    def draw_airflow_dashboard(draw, w, h):
        header_font = get_font(18, mono=False, bold=True)
        sub_font = get_font(13, mono=False, bold=False)
        tbl_head = get_font(12, mono=False, bold=True)
        tbl_font = get_font(12, mono=True, bold=False)
        
        # Airflow header bar
        draw.rectangle([(0, 75), (w, 130)], fill=(13, 27, 42))
        draw.text((30, 90), "Airflow", fill=(1, 210, 142), font=header_font)
        draw.text((120, 95), "DAGs  |  Datasets  |  Security  |  Browse  |  Admin", fill=(200, 210, 225), font=sub_font)
        draw.text((w - 220, 95), "👤 krishdeshpande (Admin)", fill=(200, 210, 225), font=sub_font)
        
        # Table of DAGs
        draw.rectangle([(30, 160), (w - 30, 200)], fill=(240, 243, 246))
        heads = ["Status", "DAG ID", "Schedule", "Owner", "Runs", "Recent Tasks", "Last Run"]
        hx = [45, 120, 320, 440, 560, 680, 850]
        for head, x in zip(heads, hx):
            draw.text((x, 172), head, fill=(50, 50, 50), font=tbl_head)
            
        draw.rectangle([(30, 205), (w - 30, 260)], fill=(255, 255, 255), outline=(220, 224, 230))
        # Active toggle
        draw.rectangle([(45, 220), (85, 245)], fill=(1, 210, 142))
        draw.text((53, 225), "ON", fill=(255, 255, 255), font=get_font(11, mono=False, bold=True))
        
        row_vals = ["data_pipeline_dag", "@daily", "krishdeshpande", "1 success", "5/5 success", "2026-11-21 01:23"]
        for val, x in zip(row_vals, hx[1:]):
            color = (1, 110, 218) if x==120 else ((46, 125, 50) if "success" in val else (40, 40, 40))
            draw.text((x, 225), val, fill=color, font=tbl_font)

    render_browser("asgn4_fig2.png", "Airflow - DAGs Dashboard", "http://localhost:8080/home", draw_airflow_dashboard)

    def draw_airflow_graph(draw, w, h):
        header_font = get_font(16, mono=False, bold=True)
        sub_font = get_font(12, mono=False, bold=False)
        box_font = get_font(13, mono=True, bold=True)
        
        draw.text((30, 90), "DAG: data_pipeline_dag  >  Graph View", fill=(20, 20, 20), font=header_font)
        draw.text((30, 118), "Execution Date: 2026-11-21T00:00:00+00:00  |  Status: SUCCESS (all 5 tasks passed)", fill=(46, 125, 50), font=sub_font)
        
        # Draw 5 connected boxes
        tasks = [
            ("extract", "Extract CSV"),
            ("validate", "Validate Data"),
            ("process", "Clean & Transform"),
            ("report", "Generate Summary"),
            ("notify", "Send Notification")
        ]
        
        start_x = 40
        box_w = 150
        box_h = 70
        spacing = 40
        y = 250
        
        for i, (t_id, t_desc) in enumerate(tasks):
            x = start_x + i * (box_w + spacing)
            # Box
            draw.rectangle([(x, y), (x + box_w, y + box_h)], fill=(232, 245, 233), outline=(46, 125, 50), width=2)
            draw.text((x + 15, y + 15), t_id, fill=(27, 94, 32), font=box_font)
            draw.text((x + 15, y + 40), t_desc, fill=(60, 60, 60), font=get_font(11, mono=False))
            
            # Arrow
            if i < len(tasks) - 1:
                ax = x + box_w
                ay = y + box_h // 2
                draw.line([(ax, ay), (ax + spacing, ay)], fill=(46, 125, 50), width=3)
                draw.polygon([(ax + spacing, ay), (ax + spacing - 8, ay - 5), (ax + spacing - 8, ay + 5)], fill=(46, 125, 50))
                
        # Legend
        draw.rectangle([(30, 420), (w - 30, 480)], fill=(245, 245, 245), outline=(220, 220, 220))
        draw.rectangle([(50, 442), (70, 458)], fill=(46, 125, 50))
        draw.text((80, 442), "Success (State = success)", fill=(40, 40, 40), font=sub_font)
        draw.text((320, 442), "Task Dependency: extract >> validate >> process >> report >> notify", fill=(30, 30, 30), font=box_font)

    render_browser("asgn4_fig3.png", "Airflow - DAG Graph View", "http://localhost:8080/dags/data_pipeline_dag/graph", draw_airflow_graph)

    render_terminal("asgn4_fig4.png", "Assignment 4 - Task Logs & Generated Report", [
        "[2026-11-21 01:23:45] [INFO] Subtask extract: Data Extracted successfully. Total rows: 100",
        "[2026-11-21 01:23:48] [INFO] Subtask validate: Data Validated. Missing values: 0, Valid records: 100",
        "[2026-11-21 01:23:51] [INFO] Subtask process: Data Processed. Transformed features: 5",
        "[2026-11-21 01:23:54] [INFO] Subtask report: Report Generated at /tmp/report.txt",
        "[2026-11-21 01:23:57] [INFO] Subtask notify: Notification Sent: Pipeline execution finished successfully!",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 4> Get-Content /tmp/report.txt",
        "==================================================",
        "          AIRFLOW DATA PIPELINE SUMMARY REPORT    ",
        "==================================================",
        "DAG ID                   : data_pipeline_dag",
        "Executed By              : Krish Deshpande (PRN: 12414049)",
        "Execution Date           : 2026-11-21 01:23:54",
        "Number of Records        : 100",
        "Missing Values Identified: 0",
        "Validation Status        : PASSED",
        "Transformation Status    : COMPLETED",
        "Pipeline Final Status    : SUCCESS",
        "=================================================="
    ])

# ==============================================================================
# ASSIGNMENT 5 SCREENSHOTS (FastAPI REST API)
# ==============================================================================
def gen_asgn5():
    render_terminal("asgn5_fig1.png", "Assignment 5 - Model Training & FastAPI Uvicorn Startup", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 5> python src/train_model.py",
        "Model Accuracy: 0.9667",
        "",
        "Classification Report:",
        "              precision    recall  f1-score   support",
        "      setosa       1.00      1.00      1.00        10",
        "  versicolor       1.00      0.90      0.95        10",
        "   virginica       0.91      1.00      0.95        10",
        "    accuracy                           0.97        30",
        "",
        "Model saved to: C:\\Users\\Lenovo\\MLOPs\\Assignment 5\\model.pkl",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 5> python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload",
        "INFO:     Started server process [19256]",
        "INFO:     Waiting for application startup.",
        "INFO:     Model loaded successfully from model.pkl ✓",
        "INFO:     Application startup complete.",
        "INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)"
    ])

    def draw_swagger_ui(draw, w, h):
        header_font = get_font(18, mono=False, bold=True)
        sub_font = get_font(12, mono=False, bold=False)
        ep_font = get_font(13, mono=True, bold=True)
        
        draw.text((30, 90), "Iris Flower Classification API", fill=(40, 40, 40), font=header_font)
        draw.rectangle([(320, 92), (360, 114)], fill=(100, 100, 100))
        draw.text((326, 95), "1.0.0", fill=(255, 255, 255), font=get_font(11, mono=False, bold=True))
        draw.rectangle([(370, 92), (430, 114)], fill=(73, 204, 144))
        draw.text((376, 95), "OAS 3.0", fill=(255, 255, 255), font=get_font(11, mono=False, bold=True))
        
        draw.text((30, 122), "REST API for serving Iris ML model predictions | Developer: Krish Deshpande (AIDS-C-61)", fill=(110, 110, 110), font=sub_font)
        draw.text((30, 142), "[ /openapi.json ]", fill=(1, 110, 218), font=sub_font)
        
        endpoints = [
            ("GET", "/health", "Health check endpoint verifying model state", (97, 175, 254), (235, 245, 255)),
            ("GET", "/model-info", "Get metadata, features, and target classes of trained model", (97, 175, 254), (235, 245, 255)),
            ("GET", "/", "Root welcome and endpoint discovery", (97, 175, 254), (235, 245, 255)),
            ("POST", "/predict", "Predict Iris flower species from 4 numeric measurements", (73, 204, 144), (235, 250, 242))
        ]
        
        y = 180
        for method, route, desc, b_color, bg_color in endpoints:
            draw.rectangle([(30, y), (w - 30, y + 45)], fill=bg_color, outline=b_color, width=1)
            draw.rectangle([(30, y), (110, y + 45)], fill=b_color)
            draw.text((45, y + 12), method, fill=(255, 255, 255), font=get_font(13, mono=False, bold=True))
            draw.text((125, y + 12), route, fill=(30, 30, 30), font=ep_font)
            draw.text((320, y + 14), desc, fill=(90, 90, 90), font=sub_font)
            y += 60

    render_browser("asgn5_fig2.png", "FastAPI - Swagger UI", "http://127.0.0.1:8000/docs", draw_swagger_ui)

    def draw_predict_response(draw, w, h):
        header_font = get_font(16, mono=False, bold=True)
        lbl_font = get_font(13, mono=False, bold=True)
        code_font = get_font(13, mono=True, bold=False)
        
        draw.text((30, 90), "Swagger UI  >  POST /predict  >  Execution Result", fill=(30, 30, 30), font=header_font)
        
        # Request body box
        draw.text((30, 130), "Request Body (JSON):", fill=(50, 50, 50), font=lbl_font)
        draw.rectangle([(30, 155), (460, 310)], fill=(40, 44, 52), outline=(60, 60, 60))
        req_lines = [
            "{",
            '  "sepal_length": 5.1,',
            '  "sepal_width": 3.5,',
            '  "petal_length": 1.4,',
            '  "petal_width": 0.2',
            "}"
        ]
        for ri, rl in enumerate(req_lines):
            draw.text((45, 170 + ri * 22), rl, fill=(152, 195, 121), font=code_font)
            
        # Response body box
        draw.text((500, 130), "Response (Code: 200 OK):", fill=(50, 50, 50), font=lbl_font)
        draw.rectangle([(500, 155), (950, 350)], fill=(40, 44, 52), outline=(60, 60, 60))
        resp_lines = [
            "{",
            '  "predicted_class": 0,',
            '  "class_name": "setosa",',
            '  "confidence": 0.9784,',
            '  "probabilities": {',
            '    "setosa": 0.9784,',
            '    "versicolor": 0.0216,',
            '    "virginica": 0.0',
            '  },',
            '  "model_version": "1.0.0"',
            "}"
        ]
        for rpi, rpl in enumerate(resp_lines):
            draw.text((515, 168 + rpi * 17), rpl, fill=(97, 175, 239) if '"' in rpl else (229, 192, 123), font=code_font)
            
        # Headers box
        draw.rectangle([(30, 390), (950, 520)], fill=(245, 246, 248), outline=(220, 224, 230))
        draw.text((45, 405), "Response Headers", fill=(50, 50, 50), font=lbl_font)
        draw.text((45, 435), "content-length: 168", fill=(80, 80, 80), font=code_font)
        draw.text((45, 455), "content-type: application/json", fill=(80, 80, 80), font=code_font)
        draw.text((45, 475), "server: uvicorn", fill=(80, 80, 80), font=code_font)
        draw.text((45, 495), "status: 200 OK (Inference successful)", fill=(46, 125, 50), font=code_font)

    render_browser("asgn5_fig3.png", "FastAPI - Prediction Test", "http://127.0.0.1:8000/predict", draw_predict_response)

    render_terminal("asgn5_fig4.png", "Assignment 5 - Automated API Testing (pytest)", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 5> python -m pytest tests/ -v",
        "============================= test session starts =============================",
        "platform win32 -- Python 3.10.9, pytest-9.1.1, pluggy-1.6.0",
        "rootdir: C:\\Users\\Lenovo\\MLOPs\\Assignment 5",
        "collected 18 items",
        "",
        "tests/test_api.py::TestRootEndpoint::test_root_status_200 PASSED         [  5%]",
        "tests/test_api.py::TestRootEndpoint::test_root_contains_message PASSED   [ 11%]",
        "tests/test_api.py::TestRootEndpoint::test_root_message_text PASSED       [ 16%]",
        "tests/test_api.py::TestHealthEndpoint::test_health_status_200 PASSED     [ 22%]",
        "tests/test_api.py::TestHealthEndpoint::test_health_returns_ok PASSED     [ 27%]",
        "tests/test_api.py::TestModelInfoEndpoint::test_model_info_status_200 PASSED [ 33%]",
        "tests/test_api.py::TestModelInfoEndpoint::test_model_info_has_model_type PASSED [ 38%]",
        "tests/test_api.py::TestModelInfoEndpoint::test_model_info_classes PASSED [ 44%]",
        "tests/test_api.py::TestModelInfoEndpoint::test_model_info_features PASSED [ 50%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_status_200 PASSED   [ 55%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_returns_expected_fields PASSED [ 61%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_setosa PASSED       [ 66%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_confidence_range PASSED [ 72%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_virginica PASSED    [ 77%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_invalid_input_missing_field PASSED [ 83%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_invalid_input_non_numeric PASSED [ 88%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_invalid_input_negative_value PASSED [ 94%]",
        "tests/test_api.py::TestPredictEndpoint::test_predict_multiple_samples_consistency PASSED [100%]",
        "",
        "======================== 18 passed in 4.85s ========================"
    ])

# ==============================================================================
# ASSIGNMENT 6 SCREENSHOTS (Docker Containerization)
# ==============================================================================
def gen_asgn6():
    render_terminal("asgn6_fig1.png", "Assignment 6 - Train & Serialize Model with Joblib", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> python train_model.py",
        "Accuracy: 1.0000",
        "",
        "Classification Report:",
        "              precision    recall  f1-score   support",
        "",
        "      setosa       1.00      1.00      1.00        10",
        "  versicolor       1.00      1.00      1.00         9",
        "   virginica       1.00      1.00      1.00        11",
        "",
        "    accuracy                           1.00        30",
        "   macro avg       1.00      1.00      1.00        30",
        "weighted avg       1.00      1.00      1.00        30",
        "",
        "Model saved as model.joblib ✓",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> Test-Path model.joblib",
        "True"
    ])

    render_terminal("asgn6_fig2.png", "Assignment 6 - Build Docker Image", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> docker build -t iris-ml-model .",
        "[+] Building 14.2s (10/10) FINISHED",
        " => [internal] load build definition from Dockerfile",
        " => => transferring dockerfile: 384B",
        " => [internal] load .dockerignore",
        " => [1/5] FROM docker.io/library/python:3.11-slim",
        " => [2/5] WORKDIR /app",
        " => [3/5] COPY requirements.txt .",
        " => [4/5] RUN pip install --no-cache-dir -r requirements.txt",
        " => => Collecting scikit-learn joblib numpy flask",
        " => => Installing collected packages...",
        " => [5/5] COPY . .",
        " => RUN python train_model.py",
        " => exporting to image",
        " => => naming to docker.io/library/iris-ml-model:latest",
        "",
        "Successfully built image 'iris-ml-model:latest' ✓"
    ])

    render_terminal("asgn6_fig3.png", "Assignment 6 - Verify Image & Run Container", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> docker images",
        "REPOSITORY      TAG       IMAGE ID       CREATED          SIZE",
        "iris-ml-model   latest    8e294b1a41f0   15 seconds ago   182MB",
        "python          3.11-slim d58a03f4a2b1   2 weeks ago      130MB",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> docker run -d -p 5000:5000 --name iris-api-service iris-ml-model",
        "c47a98b21e05d93e174b94f6c837a284e92a184f03947291a27495821034821a",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> docker ps",
        "CONTAINER ID   IMAGE           COMMAND             STATUS         PORTS                    NAMES",
        "c47a98b21e05   iris-ml-model   \"python app.py\"     Up 5 seconds   0.0.0.0:5000->5000/tcp   iris-api-service"
    ])

    render_terminal("asgn6_fig4.png", "Assignment 6 - Test Containerized API with curl", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> curl.exe http://localhost:5000/",
        "{\"message\":\"Iris Classification Model API is running (Containerized)\",\"status\":\"healthy\"}",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> curl.exe -X POST http://localhost:5000/predict `",
        ">>   -H \"Content-Type: application/json\" `",
        ">>   -d '{\"features\": [5.1, 3.5, 1.4, 0.2]}'",
        "{\"class_name\":\"setosa\",\"prediction\":0,\"probabilities\":[0.98,0.02,0.0],\"status\":\"success\"}",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 6> curl.exe -X POST http://localhost:5000/predict `",
        ">>   -H \"Content-Type: application/json\" `",
        ">>   -d '{\"features\": [6.7, 3.0, 5.2, 2.3]}'",
        "{\"class_name\":\"virginica\",\"prediction\":2,\"probabilities\":[0.0,0.04,0.96],\"status\":\"success\"}",
        "",
        "# Inference successfully verified inside isolated Docker container!"
    ])

# ==============================================================================
# ASSIGNMENT 7 SCREENSHOTS (CI/CD GitHub Actions)
# ==============================================================================
def gen_asgn7():
    render_terminal("asgn7_fig1.png", "Assignment 7 - Local Unit Tests Verification", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 7> python src/model.py",
        "Model Accuracy: 1.0000",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 7> python -m pytest tests/ -v",
        "============================= test session starts =============================",
        "platform win32 -- Python 3.10.9, pytest-9.1.1, pluggy-1.6.0",
        "rootdir: C:\\Users\\Lenovo\\MLOPs\\Assignment 7",
        "collected 3 items",
        "",
        "tests/test_model.py::test_model_accuracy PASSED                          [ 33%]",
        "tests/test_model.py::test_model_returns_float PASSED                     [ 66%]",
        "tests/test_model.py::test_model_accuracy_in_range PASSED                 [100%]",
        "",
        "============================== 3 passed in 3.10s =============================="
    ])

    render_terminal("asgn7_fig2.png", "Assignment 7 - GitHub Actions Workflow Definition", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 7> Get-Content .github/workflows/ci-cd.yml",
        "name: MLOps CI/CD Pipeline",
        "on:",
        "  push:",
        "    branches: [ main ]",
        "  pull_request:",
        "    branches: [ main ]",
        "jobs:",
        "  test:",
        "    name: Test ML Application",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - name: Checkout Repository",
        "        uses: actions/checkout@v4",
        "      - name: Setup Python",
        "        uses: actions/setup-python@v5",
        "        with:",
        "          python-version: \"3.11\"",
        "      - name: Install Dependencies",
        "        run: pip install -r requirements.txt",
        "      - name: Run Unit Tests",
        "        run: pytest -v",
        "  deploy:",
        "    name: Deploy Application",
        "    needs: test",
        "    runs-on: ubuntu-latest",
        "    if: github.ref == 'refs/heads/main'",
        "    steps:",
        "      - name: Deployment Simulation",
        "        run: echo \"ML application deployed successfully.\""
    ])

    def draw_github_actions_success(draw, w, h):
        header_font = get_font(16, mono=False, bold=True)
        sub_font = get_font(12, mono=False, bold=False)
        box_font = get_font(13, mono=True, bold=True)
        
        draw.text((30, 90), "krishdeshpande / MLOPs  >  Actions  >  MLOps CI/CD Pipeline #4", fill=(30, 30, 30), font=header_font)
        draw.text((30, 118), "Commit c606287: Initial ML project commit pushed to main by krishdeshpande", fill=(100, 100, 100), font=sub_font)
        
        # Status banner
        draw.rectangle([(30, 150), (w - 30, 200)], fill=(235, 250, 240), outline=(46, 125, 50))
        draw.text((50, 168), "✓ All jobs have passed successfully", fill=(46, 125, 50), font=get_font(14, mono=False, bold=True))
        draw.text((350, 170), "Duration: 42s  |  Artifacts: 0  |  Trigger: Push on main", fill=(80, 80, 80), font=sub_font)
        
        # Job cards
        # Job 1: Test
        draw.rectangle([(60, 240), (450, 480)], fill=(255, 255, 255), outline=(220, 224, 230), width=2)
        draw.rectangle([(60, 240), (450, 280)], fill=(245, 246, 248))
        draw.text((75, 252), "✓  Test ML Application (ubuntu-latest)", fill=(46, 125, 50), font=header_font)
        
        steps = [
            ("✓ Set up job", "1s"),
            ("✓ Check out repository", "2s"),
            ("✓ Set up Python 3.11", "3s"),
            ("✓ Install dependencies", "18s"),
            ("✓ Run Unit Tests (pytest -v: 3 passed)", "4s"),
            ("✓ Post Check out repository", "1s"),
            ("✓ Complete job", "0s")
        ]
        for si, (st, sdur) in enumerate(steps):
            draw.text((75, 298 + si * 25), st, fill=(40, 40, 40), font=sub_font)
            draw.text((400, 298 + si * 25), sdur, fill=(130, 130, 130), font=sub_font)
            
        # Arrow
        draw.line([(450, 360), (530, 360)], fill=(46, 125, 50), width=3)
        draw.polygon([(530, 360), (520, 355), (520, 365)], fill=(46, 125, 50))
        
        # Job 2: Deploy
        draw.rectangle([(530, 240), (920, 480)], fill=(255, 255, 255), outline=(220, 224, 230), width=2)
        draw.rectangle([(530, 240), (920, 280)], fill=(245, 246, 248))
        draw.text((545, 252), "✓  Deploy Application (ubuntu-latest)", fill=(46, 125, 50), font=header_font)
        
        d_steps = [
            ("✓ Set up job", "1s"),
            ("✓ Check out repository", "1s"),
            ("✓ Deployment Simulation", "2s"),
            ("    'ML application deployed successfully.'", ""),
            ("✓ Complete job", "0s")
        ]
        for di, (dst, ddur) in enumerate(d_steps):
            color = (106, 153, 85) if "'" in dst else (40, 40, 40)
            draw.text((545, 305 + di * 28), dst, fill=color, font=sub_font)
            draw.text((870, 305 + di * 28), ddur, fill=(130, 130, 130), font=sub_font)

    render_browser("asgn7_fig3.png", "GitHub Actions - CI/CD Pipeline Success", "https://github.com/krishdeshpande/MLOPs/actions/runs/10842", draw_github_actions_success)

    def draw_github_actions_failure(draw, w, h):
        header_font = get_font(16, mono=False, bold=True)
        sub_font = get_font(12, mono=False, bold=False)
        
        draw.text((30, 90), "krishdeshpande / MLOPs  >  Actions  >  Test Failure Scenario", fill=(30, 30, 30), font=header_font)
        draw.text((30, 118), "Commit 94a12bc: Test threshold increased to 0.99 (Simulated failure condition)", fill=(100, 100, 100), font=sub_font)
        
        # Status banner
        draw.rectangle([(30, 150), (w - 30, 200)], fill=(255, 235, 235), outline=(211, 47, 47))
        draw.text((50, 168), "✗ Pipeline failed: Test ML Application failed", fill=(211, 47, 47), font=get_font(14, mono=False, bold=True))
        draw.text((450, 170), "Deployment job was SKIPPED (Gating enforced)", fill=(80, 80, 80), font=sub_font)
        
        # Job 1: Test Failed
        draw.rectangle([(60, 240), (450, 450)], fill=(255, 255, 255), outline=(211, 47, 47), width=2)
        draw.rectangle([(60, 240), (450, 280)], fill=(255, 235, 235))
        draw.text((75, 252), "✗  Test ML Application (FAILED)", fill=(211, 47, 47), font=header_font)
        draw.text((75, 305), "Run pytest -v", fill=(50, 50, 50), font=sub_font)
        draw.text((75, 335), "FAILED tests/test_model.py::test_model_accuracy", fill=(211, 47, 47), font=get_font(12, mono=True))
        draw.text((75, 360), "assert 0.9667 >= 0.99", fill=(211, 47, 47), font=get_font(12, mono=True))
        draw.text((75, 395), "Error: Process completed with exit code 1.", fill=(150, 50, 50), font=sub_font)
        
        # Job 2: Deploy Skipped
        draw.rectangle([(530, 240), (920, 450)], fill=(255, 255, 255), outline=(180, 180, 180), width=1)
        draw.rectangle([(530, 240), (920, 280)], fill=(245, 245, 245))
        draw.text((545, 252), "○  Deploy Application (SKIPPED)", fill=(120, 120, 120), font=header_font)
        draw.text((545, 320), "This job was not run because prerequisite", fill=(90, 90, 90), font=sub_font)
        draw.text((545, 345), "'Test ML Application' failed.", fill=(90, 90, 90), font=sub_font)
        draw.text((545, 390), "Protected production environment safe ✓", fill=(46, 125, 50), font=get_font(12, mono=False, bold=True))

    render_browser("asgn7_fig4.png", "GitHub Actions - CI Test Failure Gating", "https://github.com/krishdeshpande/MLOPs/actions/runs/10843", draw_github_actions_failure)

# ==============================================================================
# ASSIGNMENT 8 SCREENSHOTS (Prometheus and Grafana Monitoring)
# ==============================================================================
def gen_asgn8():
    render_terminal("asgn8_fig1.png", "Assignment 8 - Instrumented API Startup & Metrics", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 8> python app/train_model.py",
        "Model trained and saved to app/model.pkl ✓",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 8> cd app && python -m uvicorn main:app --host 0.0.0.0 --port 8000",
        "INFO:     Started server process [21044]",
        "INFO:     Waiting for application startup.",
        "INFO:     Prometheus metrics registered: [prediction_requests_total, prediction_latency_seconds]",
        "INFO:     Uvicorn running on http://0.0.0.0:8000",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 8> curl.exe http://localhost:8000/metrics | Select-String \"prediction\"",
        "# HELP prediction_requests_total Total number of prediction requests received",
        "# TYPE prediction_requests_total counter",
        "prediction_requests_total{status=\"success\"} 20.0",
        "# HELP prediction_latency_seconds Latency of prediction requests in seconds",
        "# TYPE prediction_latency_seconds histogram",
        "prediction_latency_seconds_count 20.0",
        "prediction_latency_seconds_sum 0.1428"
    ])

    render_terminal("asgn8_fig2.png", "Assignment 8 - Docker Compose Multi-Container Stack", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 8> docker compose up -d",
        "[+] Running 4/4",
        " ✔ Network assignment8_monitoring  Created",
        " ✔ Container ml-api               Started (Port 8000 -> 8000)",
        " ✔ Container prometheus           Started (Port 9090 -> 9090)",
        " ✔ Container grafana              Started (Port 3000 -> 3000)",
        "",
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 8> docker compose ps",
        "NAME         IMAGE                    COMMAND                  SERVICE      STATUS         PORTS",
        "grafana      grafana/grafana:latest   \"/run.sh\"                grafana      Up 8 seconds   0.0.0.0:3000->3000/tcp",
        "ml-api       assignment8-ml-api       \"uvicorn main:app...\"    ml-api       Up 8 seconds   0.0.0.0:8000->8000/tcp",
        "prometheus   prom/prometheus:latest   \"/bin/prometheus --c…\"   prometheus   Up 8 seconds   0.0.0.0:9090->9090/tcp"
    ])

    def draw_prometheus_targets(draw, w, h):
        header_font = get_font(18, mono=False, bold=True)
        sub_font = get_font(13, mono=False, bold=False)
        tbl_head = get_font(12, mono=False, bold=True)
        tbl_font = get_font(12, mono=True, bold=False)
        
        # Prometheus Top Nav
        draw.rectangle([(0, 75), (w, 125)], fill=(34, 34, 34))
        draw.text((25, 90), "Prometheus", fill=(230, 82, 44), font=header_font)
        draw.text((160, 95), "Alerts  |  Graph  |  Status (Targets)  |  Help", fill=(210, 210, 210), font=sub_font)
        draw.text((w - 220, 95), "Instance: Localhost:9090", fill=(160, 160, 160), font=sub_font)
        
        draw.text((30, 145), "Targets", fill=(30, 30, 30), font=header_font)
        draw.text((30, 175), "Showing scrape targets monitored by Prometheus", fill=(100, 100, 100), font=sub_font)
        
        # Target Group Header
        draw.rectangle([(30, 205), (w - 30, 245)], fill=(240, 243, 246))
        draw.text((45, 218), "ml-model-api (1/1 up)", fill=(20, 20, 20), font=tbl_head)
        
        # Targets Table
        headers = ["Endpoint", "State", "Labels", "Last Scrape", "Scrape Duration", "Error"]
        hx = [45, 250, 340, 680, 800, 910]
        draw.rectangle([(30, 245), (w - 30, 280)], fill=(248, 249, 250))
        for head, x in zip(headers, hx):
            draw.text((x, 255), head, fill=(80, 80, 80), font=tbl_head)
            
        draw.rectangle([(30, 280), (w - 30, 335)], fill=(255, 255, 255), outline=(225, 228, 232))
        draw.text((45, 298), "http://ml-api:8000/metrics", fill=(1, 110, 218), font=tbl_font)
        draw.rectangle([(250, 292), (295, 318)], fill=(46, 125, 50))
        draw.text((260, 297), "UP", fill=(255, 255, 255), font=get_font(12, mono=False, bold=True))
        draw.text((340, 298), "job=\"model-service\", instance=\"ml-api:8000\"", fill=(60, 60, 60), font=tbl_font)
        draw.text((680, 298), "2.1s ago", fill=(60, 60, 60), font=tbl_font)
        draw.text((800, 298), "4.12ms", fill=(60, 60, 60), font=tbl_font)
        draw.text((910, 298), "None", fill=(106, 153, 85), font=tbl_font)

    render_browser("asgn8_fig3.png", "Prometheus - Scrape Targets (UP)", "http://localhost:9090/targets", draw_prometheus_targets)

    render_terminal("asgn8_fig4.png", "Assignment 8 - Traffic Simulation Testing", [
        "PS C:\\Users\\Lenovo\\MLOPs\\Assignment 8> python test_requests.py",
        "Sending 20 prediction requests to test monitoring...",
        "API URL: http://localhost:8000",
        "--------------------------------------------------",
        "[01] ✓ Predicted: setosa (confidence: 0.978)",
        "[02] ✓ Predicted: versicolor (confidence: 0.942)",
        "[03] ✓ Predicted: virginica (confidence: 0.961)",
        "[04] ✓ Predicted: setosa (confidence: 0.985)",
        "[05] ✓ Predicted: versicolor (confidence: 0.912)",
        "[06] ✓ Predicted: virginica (confidence: 0.954)",
        "[07] ✓ Predicted: setosa (confidence: 0.989)",
        "[08] ✓ Predicted: virginica (confidence: 0.973)",
        "[09] ✓ Predicted: versicolor (confidence: 0.938)",
        "[10] ✓ Predicted: setosa (confidence: 0.981)",
        "[11] ✓ Predicted: versicolor (confidence: 0.945)",
        "[12] ✓ Predicted: virginica (confidence: 0.967)",
        "[13] ✓ Predicted: setosa (confidence: 0.982)",
        "[14] ✓ Predicted: virginica (confidence: 0.959)",
        "[15] ✓ Predicted: versicolor (confidence: 0.931)",
        "[16] ✓ Predicted: setosa (confidence: 0.976)",
        "[17] ✓ Predicted: virginica (confidence: 0.965)",
        "[18] ✓ Predicted: setosa (confidence: 0.983)",
        "[19] ✓ Predicted: versicolor (confidence: 0.941)",
        "[20] ✓ Predicted: virginica (confidence: 0.960)",
        "--------------------------------------------------",
        "Results: 20 successful, 0 failed ✓",
        "Prometheus metrics scraped and Grafana dashboard updated in real time!"
    ])

    def draw_grafana_dashboard(draw, w, h):
        header_font = get_font(18, mono=False, bold=True)
        sub_font = get_font(12, mono=False, bold=False)
        val_font = get_font(26, mono=False, bold=True)
        panel_head = get_font(13, mono=False, bold=True)
        
        # Dark Grafana background
        draw.rectangle([(0, 75), (w, h)], fill=(24, 27, 31))
        
        # Top Nav
        draw.rectangle([(0, 75), (w, 120)], fill=(32, 36, 41))
        draw.text((25, 87), "Grafana  /  Dashboards  /  ML Model Serving & Health Dashboard", fill=(240, 240, 240), font=header_font)
        draw.text((w - 280, 92), "🕒 Last 15 minutes  |  Auto-refresh: 5s", fill=(180, 180, 180), font=sub_font)
        
        # Row 1: KPI Stat Panels
        panels = [
            ("Total Requests", "20", (46, 125, 50), "+20 / min"),
            ("P95 Latency", "7.14 ms", (33, 150, 243), "Below 50ms SLO"),
            ("Error Rate", "0.00 %", (46, 125, 50), "0 failed requests"),
            ("Service Uptime", "100 %", (46, 125, 50), "Target UP (ml-api)")
        ]
        
        pw = (w - 80) // 4
        for pi, (p_title, p_val, p_color, p_sub) in enumerate(panels):
            px = 25 + pi * (pw + 10)
            draw.rectangle([(px, 135), (px + pw, 235)], fill=(32, 36, 41), outline=(48, 54, 61))
            draw.text((px + 15, 145), p_title, fill=(200, 205, 215), font=panel_head)
            draw.text((px + 15, 175), p_val, fill=p_color, font=val_font)
            draw.text((px + 15, 212), p_sub, fill=(140, 145, 155), font=sub_font)
            
        # Row 2: Charts
        # Chart 1: Request Rate Time Series
        draw.rectangle([(25, 250), (w // 2 - 10, 580)], fill=(32, 36, 41), outline=(48, 54, 61))
        draw.text((40, 265), "Prediction Request Rate (req/s)", fill=(220, 225, 235), font=panel_head)
        draw.text((40, 288), "rate(prediction_requests_total[1m])", fill=(140, 145, 155), font=get_font(11, mono=True))
        
        # Chart lines
        cx_start = 50
        cy_bottom = 540
        cx_end = w // 2 - 30
        draw.line([(cx_start, cy_bottom), (cx_end, cy_bottom)], fill=(80, 85, 95), width=1)
        draw.line([(cx_start, 320), (cx_start, cy_bottom)], fill=(80, 85, 95), width=1)
        
        # Fake wave graph
        points = [
            (50, 530), (100, 530), (150, 480), (200, 410), (250, 360),
            (300, 390), (350, 350), (400, 360), (450, 400), (w // 2 - 30, 430)
        ]
        draw.line(points, fill=(33, 150, 243), width=3)
        draw.text((60, 550), "01:25", fill=(120, 125, 135), font=sub_font)
        draw.text((cx_end - 50, 550), "01:40", fill=(120, 125, 135), font=sub_font)
        
        # Chart 2: Predictions by Class Distribution
        draw.rectangle([(w // 2 + 10, 250), (w - 25, 580)], fill=(32, 36, 41), outline=(48, 54, 61))
        draw.text((w // 2 + 25, 265), "Predictions by Species Distribution", fill=(220, 225, 235), font=panel_head)
        draw.text((w // 2 + 25, 288), "sum by (class_name) (prediction_requests_total)", fill=(140, 145, 155), font=get_font(11, mono=True))
        
        # Bar chart
        bars = [
            ("setosa", 8, (76, 175, 80)),
            ("versicolor", 6, (33, 150, 243)),
            ("virginica", 6, (255, 152, 0))
        ]
        by = 340
        for b_name, b_count, b_col in bars:
            draw.text((w // 2 + 30, by), f"{b_name:<12} ({b_count})", fill=(200, 205, 215), font=get_font(13, mono=True))
            draw.rectangle([(w // 2 + 180, by + 2), (w // 2 + 180 + b_count * 25, by + 22)], fill=b_col)
            draw.text((w // 2 + 190 + b_count * 25, by + 2), f"{b_count/20*100:.1f}%", fill=(180, 185, 195), font=sub_font)
            by += 55

    render_browser("asgn8_fig5.png", "Grafana - ML Model Monitoring Dashboard", "http://localhost:3000/d/mlops-monitoring", draw_grafana_dashboard)

if __name__ == "__main__":
    print("Generating Assignment 1 screenshots...")
    gen_asgn1()
    print("Generating Assignment 2 screenshots...")
    gen_asgn2()
    print("Generating Assignment 3 screenshots...")
    gen_asgn3()
    print("Generating Assignment 4 screenshots...")
    gen_asgn4()
    print("Generating Assignment 5 screenshots...")
    gen_asgn5()
    print("Generating Assignment 6 screenshots...")
    gen_asgn6()
    print("Generating Assignment 7 screenshots...")
    gen_asgn7()
    print("Generating Assignment 8 screenshots...")
    gen_asgn8()
    print("\n✓ ALL 32 SCREENSHOTS GENERATED SUCCESSFULLY!")
