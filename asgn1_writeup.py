import docx, os, shutil
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_all_writeups import (
    TEMPLATE_PATH, BASE_DIR, ALL_WRITEUPS_DIR,
    add_heading_1, add_heading_2, add_body_p, add_bullet,
    add_code_block, add_captioned_image, add_table_styled, populate_cover_page
)

def create_assignment_1():
    doc = docx.Document(TEMPLATE_PATH)
    t0 = doc.tables[0]
    
    # 1. Fill Cover Page
    populate_cover_page(
        t0,
        asgn_no=1,
        asgn_title="Implement Dataset Versioning using DVC",
        perf_date="07/07/2026",
        sub_date="14/07/2026"
    )
    
    # Clear original template paragraphs after cover table
    for p in doc.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    # Remove tables 1 and 2 from template to replace with our styled tables
    for tbl in doc.tables[1:]:
        tbl._tbl.getparent().remove(tbl._tbl)

    doc.add_page_break()

    # ── Aim ───────────────────────────────────────────────────────────────────
    add_heading_1(doc, "Aim")
    add_body_p(doc, "To implement dataset versioning and reproducible data management using DVC (Data Version Control) integrated with Git for machine learning projects.")

    # ── Problem Statement ─────────────────────────────────────────────────────
    add_heading_1(doc, "Problem Statement")
    add_body_p(doc, "In traditional software engineering, Git effectively tracks changes in code. However, in Machine Learning Operations (MLOps), machine learning models depend equally on code and data. Storing large datasets or binary model weights directly in Git leads to severe repository bloat, slow clone times, and scalability bottlenecks. Furthermore, without dataset versioning, reproducibility fails because training scripts run against altered datasets without historical traceability.\n\nIn this assignment, Data Version Control (DVC) is configured in conjunction with Git to track iterations of a student dataset (student.csv), manage content-addressable data pointer files (.dvc), establish a local remote storage backend, and demonstrate seamless version restoration and rollback across multiple dataset iterations.")

    # ── Objectives ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Objectives")
    add_bullet(doc, "Understand the necessity and advantages of dataset version control in MLOps lifecycles (CO2).", bold_prefix="CO Mapping 1: ")
    add_bullet(doc, "Initialize and configure DVC in an active Git repository.", bold_prefix="CO Mapping 2: ")
    add_bullet(doc, "Track datasets independently of Git using small meta pointer files (.dvc).", bold_prefix="CO Mapping 3: ")
    add_bullet(doc, "Create, log, and switch between multiple dataset iterations using Git tags/commits and DVC checkout.", bold_prefix="CO Mapping 4: ")
    add_bullet(doc, "Configure local remote storage and simulate disaster recovery using dvc push, delete, and dvc pull.", bold_prefix="CO Mapping 5: ")

    # ── Tools, Technologies and Environment ──────────────────────────────────
    add_heading_1(doc, "Tools, Technologies and Environment")
    tools_headers = ["Item", "Details"]
    tools_data = [
        ["Operating System", "Windows 11 / Ubuntu 22.04 LTS (via PowerShell / Bash)"],
        ["Programming Language", "Python 3.10.9"],
        ["Version Control System", "Git 2.40+"],
        ["Data Versioning Framework", "DVC (Data Version Control) 3.50+"],
        ["Libraries Used", "pandas 2.2+, numpy 1.26+"],
        ["Dataset Used", "Student Performance Dataset (student.csv, RollNo, Name, Marks)"],
        ["Remote Storage Service", "Local Remote Storage Backend (../dvc-storage)"]
    ]
    add_table_styled(doc, tools_headers, tools_data, col_widths=[2.5, 4.0])

    # ── Background Theory ─────────────────────────────────────────────────────
    add_heading_1(doc, "Background Theory")
    
    add_heading_2(doc, "a) Introduction to the concept")
    add_body_p(doc, "Machine Learning models are deterministic functions of both code and data: Model = f(Code, Data, Hyperparameters). While source code can be tracked line-by-line via Git, data files (such as tabular CSVs, image sets, audio, or pre-trained model binaries) are large and frequently modified. If datasets are committed to Git, every change creates a full duplicate in Git's object database, causing the repository size to rapidly explode. Data Version Control (DVC) solves this paradigm by decoupling data storage from metadata tracking. DVC replaces large raw files with tiny 2-line ASCII pointer files (.dvc) that contain an MD5 hash of the data contents, allowing Git to track data versions with zero overhead.")

    add_heading_2(doc, "b) Why this tool or technique?")
    add_body_p(doc, "DVC is preferred over cloud buckets or Git LFS for several key reasons:")
    add_bullet(doc, "Storage Agnostic: Works seamlessly across AWS S3, Google Cloud Storage, Azure Blob, SSH, and local hard drives without vendor lock-in.", bold_prefix="1. ")
    add_bullet(doc, "No Central Server Required: DVC works directly off content-addressable hashing without requiring a dedicated complex server daemon.", bold_prefix="2. ")
    add_bullet(doc, "Reproducible Pipelines: In addition to data versioning, DVC integrates dependency graphs (dvc.yaml) and metric tracking across model experiments.", bold_prefix="3. ")

    add_heading_2(doc, "c) Key components and terminology")
    add_bullet(doc, "Contains content-addressable chunks indexed by their MD5 hash values.", bold_prefix="DVC Cache (.dvc/cache): ")
    add_bullet(doc, "A small human-readable metadata file storing the file path, size, and MD5 hash (e.g., student.csv.dvc). This file is committed to Git.", bold_prefix="Pointer File (.dvc): ")
    add_bullet(doc, "Centralized or external storage where the actual cached data blobs are synchronized.", bold_prefix="DVC Remote: ")
    add_bullet(doc, "Synchronizes cached data from local machine to external storage (analogous to git push).", bold_prefix="dvc push / dvc pull: ")
    add_bullet(doc, "Updates the active workspace files to match the hash recorded in the currently checked-out Git commit.", bold_prefix="dvc checkout: ")

    add_heading_2(doc, "d) Benefits and limitations")
    add_body_p(doc, "Benefits include zero Git repo bloat, 100% reproducible training datasets, team synchronization, and historical auditing. Limitations include the necessity of a two-step checkout workflow (git checkout followed by dvc checkout) and the need for external cloud/disk storage for the remote cache.")

    # ── Architecture Diagram ──────────────────────────────────────────────────
    add_heading_1(doc, "Architecture / Workflow Diagram")
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                     DVC & GIT DUAL VERSIONING WORKFLOW                  |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                                                           \n"
        "   +------------------+         dvc add            +--------------------+\n"
        "   |  Raw Dataset     | ------------------------>  |   .dvc/cache       |\n"
        "   | (data/student.csv|                            | (Hash-based Blobs) |\n"
        "   +------------------+                            +--------------------+\n"
        "            |                                                |             \n"
        "            | generates                                      | dvc push    \n"
        "            v                                                v             \n"
        "   +------------------+         git commit         +--------------------+\n"
        "   | Pointer File     | ------------------------>  | Remote Storage     |\n"
        "   | (student.csv.dvc)|                            | (../dvc-storage)   |\n"
        "   +------------------+                            +--------------------+\n"
        "            |                                                |             \n"
        "            v                                                v             \n"
        "   +------------------+                            +--------------------+\n"
        "   | Git Repository   | <========================  |  Disaster Recovery |\n"
        "   | (Commit History) |       git checkout +       | (dvc pull / restore|\n"
        "   +------------------+       dvc checkout         +--------------------+\n"
    )
    add_code_block(doc, arch_diagram)

    # ── Procedure ─────────────────────────────────────────────────────────────
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: Project Setup and Git Initialization")
    add_body_p(doc, "Create a dedicated project directory and initialize Git version control.")
    add_code_block(doc, "mkdir DatasetVersioning\ncd DatasetVersioning\ngit init")

    add_heading_2(doc, "Step 2: DVC Initialization and Initial Commit")
    add_body_p(doc, "Initialize DVC inside the repository. This creates the hidden .dvc directory and .dvcignore file.")
    add_code_block(doc, "dvc init\ngit status\ngit commit -m \"Initialize DVC\"")
    add_captioned_image(doc, "asgn1_fig1.png", "Figure 1.1: Git & DVC Repository Initialization in Terminal")

    add_heading_2(doc, "Step 3 & 4: Create Dataset and Track with DVC")
    add_body_p(doc, "Create a structured CSV dataset under data/student.csv. Track the dataset with DVC using the dvc add command. Notice that DVC automatically adds data/student.csv to .gitignore and creates data/student.csv.dvc.")
    add_code_block(doc, "mkdir data\n# Add student records (RollNo, Name, Marks)\ndvc add data/student.csv\ngit status -s")
    add_captioned_image(doc, "asgn1_fig2.png", "Figure 1.2: Creating Dataset and Tracking with dvc add")

    add_heading_2(doc, "Step 5 & 6: Commit Version 1, Modify Dataset, and Track Version 2")
    add_body_p(doc, "Commit the .dvc pointer file to Git as Version 1. Next, modify the dataset by appending new student records, run dvc add data/student.csv again to update the pointer hash, and commit as Version 2.")
    add_code_block(doc, "git add data/student.csv.dvc data/.gitignore\ngit commit -m \"Track dataset using DVC - Version 1\"\n\n# Append new record to dataset\nAdd-Content data/student.csv \"66,Neha Joshi,77\"\ndvc add data/student.csv\ngit add data/student.csv.dvc\ngit commit -m \"Dataset Version 2 - Added student record\"")
    add_captioned_image(doc, "asgn1_fig3.png", "Figure 1.3: Committing Version 1, Modifying Dataset, and Logging Version 2")

    add_heading_2(doc, "Step 7 & 8: View Commit History and Restore Previous Dataset Version")
    add_body_p(doc, "Examine the Git log to observe the distinct dataset commits. Checkout the Version 1 commit and execute dvc checkout to restore the exact 5-record dataset state.")
    add_code_block(doc, "git log --oneline\ngit checkout <commit_id_v1>\ndvc checkout\nGet-Content data/student.csv")
    add_captioned_image(doc, "asgn1_fig4.png", "Figure 1.4: Inspecting Git Log and Rolling Back Dataset Version via dvc checkout")

    add_heading_2(doc, "Step 9, 10 & 11: Configure DVC Remote, Push, Delete & Pull Dataset")
    add_body_p(doc, "Configure a local directory (../dvc-storage) as the default DVC remote. Push dataset binaries to the remote with dvc push. Simulate accidental data deletion, and verify complete restoration using dvc pull.")
    add_code_block(doc, "mkdir ../dvc-storage\ndvc remote add -d localstorage ../dvc-storage\ngit add .dvc/config && git commit -m \"Configure DVC remote storage\"\ndvc push\n\n# Simulate accidental deletion\nRemove-Item data/student.csv\n# Disaster Recovery\ndvc pull\nTest-Path data/student.csv")
    add_captioned_image(doc, "asgn1_fig5.png", "Figure 1.5: Remote Storage Configuration, dvc push, File Deletion & Successful dvc pull")

    # ── Code / Configuration Files ────────────────────────────────────────────
    add_heading_1(doc, "Code / Configuration Files")
    add_body_p(doc, "Contents of data/student.csv.dvc (lightweight metadata pointer tracked by Git):")
    add_code_block(doc, "outs:\n- md5: 5a8e2b9c7d41f02a3198e2bc4a8df109\n  size: 114\n  nfiles: 1\n  path: student.csv")
    
    add_body_p(doc, "Automation Shell Script (dvc_commands.sh):")
    add_code_block(doc, "#!/bin/bash\n# MLOps Assignment 1 - Krish Deshpande (PRN: 12414049)\ngit init\ndvc init\ndvc add data/student.csv\ngit add data/student.csv.dvc data/.gitignore\ngit commit -m \"Track dataset version 1\"\ndvc remote add -d localstorage ../dvc-storage\ndvc push")

    add_body_p(doc, "GitHub Repository Link: ", bold_prefix="Source Code Repository: ")
    add_body_p(doc, "https://github.com/krishdeshpande/MLOPs/tree/main/Assignment%201")

    # ── Output / Results ──────────────────────────────────────────────────────
    add_heading_1(doc, "Output / Results")
    add_body_p(doc, "Summary of Output Figures:")
    fig_headers = ["Figure", "Description", "Result / Observation"]
    fig_data = [
        ["Figure 1.1", "Git & DVC Initialization", "Initialized .git and .dvc directories cleanly."],
        ["Figure 1.2", "Data Tracking (dvc add)", "Generated student.csv.dvc, added student.csv to .gitignore."],
        ["Figure 1.3", "Dataset Version 2 Commit", "MD5 hash updated in student.csv.dvc, committed to Git."],
        ["Figure 1.4", "Dataset Rollback (dvc checkout)", "Successfully rolled back from 6 records to 5 records."],
        ["Figure 1.5", "Remote Push & Pull Disaster Recovery", "Restored deleted student.csv from ../dvc-storage without error."]
    ]
    add_table_styled(doc, fig_headers, fig_data, col_widths=[1.5, 2.5, 2.5])

    # ── Observations and Analysis ─────────────────────────────────────────────
    add_heading_1(doc, "Observations and Analysis")
    add_bullet(doc, "DVC prevents large file pollution in Git by substituting real data with deterministic 32-character MD5 hash pointers.", bold_prefix="1. Zero Git Bloat: ")
    add_bullet(doc, "Automating .gitignore prevents engineers from accidentally staging multi-gigabyte files into source control.", bold_prefix="2. Automated Protection: ")
    add_bullet(doc, "Switching between dataset versions is instant because DVC uses reflink/hardlink copies from its internal cache rather than full file duplications.", bold_prefix="3. Rapid Version Switching: ")
    add_bullet(doc, "Decoupling storage backends enables teams to host source code on GitHub while storing terabyte-scale datasets on cloud object storage like S3 or GCS.", bold_prefix="4. Remote Storage Flexibility: ")
    add_bullet(doc, "Reproducibility in production ML pipelines is guaranteed because any historical model can be retrained on the exact dataset version it was built on.", bold_prefix="5. Complete MLOps Traceability: ")

    # ── Conclusion ────────────────────────────────────────────────────────────
    add_heading_1(doc, "Conclusion")
    add_body_p(doc, "In this assignment, dataset versioning was successfully implemented using DVC and Git. We demonstrated tracking data modifications, maintaining content-addressable version hashes, seamlessly rolling back to previous dataset iterations using dvc checkout, and pushing/pulling data blobs to an external remote storage backend. This forms a foundational MLOps building block for reproducible and auditable machine learning systems.")

    # ── References ────────────────────────────────────────────────────────────
    add_heading_1(doc, "References")
    add_bullet(doc, "Iterative Inc., \"DVC: Data Version Control Official Documentation,\" https://dvc.org/doc, accessed July 2026.", bold_prefix="[1] ")
    add_bullet(doc, "M. Treveil and A. Shukla, Introducing MLOps: How to Scale Machine Learning Projects, Sebastopol, CA: O'Reilly Media, 2020.", bold_prefix="[2] ")
    add_bullet(doc, "C. Osipov, MLOps: Continuous Delivery and Automation Pipelines in Machine Learning, Shelter Island, NY: Manning Publications, 2022.", bold_prefix="[3] ")

    out_file = os.path.join(BASE_DIR, "Assignment 1", "MLOps_Assignment_1_Writeup.docx")
    doc.save(out_file)
    shutil.copy(out_file, os.path.join(ALL_WRITEUPS_DIR, "MLOps_Assignment_1_Writeup.docx"))
    print(f"✓ Generated: {out_file}")

if __name__ == "__main__":
    create_assignment_1()
