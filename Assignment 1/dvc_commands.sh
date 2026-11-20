#!/bin/bash
# ============================================================
# Assignment 1: Dataset Versioning using DVC
# Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | AIDS Div-C
# ============================================================

# ----- STEP 1: Install DVC -----
pip install dvc

# ----- STEP 2: Initialize Git Repository -----
git init
git config user.name "Krish Deshpande"
git config user.email "krish@example.com"

# ----- STEP 3: Initialize DVC -----
dvc init

# Commit the DVC setup files
git add .dvc .dvcignore
git commit -m "Initialize DVC"

# ----- STEP 4: Add Dataset to DVC Tracking -----
mkdir -p data
# (Assumes data/student.csv already exists)

dvc add data/student.csv

# Commit the .dvc metadata file and updated .gitignore
git add data/student.csv.dvc data/.gitignore
git commit -m "Add student.csv dataset (Version 1)"

# ----- STEP 5: Configure DVC Remote Storage -----
# Using a local folder as remote (can replace with S3/GDrive path)
mkdir -p /tmp/dvc-remote
dvc remote add -d myremote /tmp/dvc-remote

git add .dvc/config
git commit -m "Configure DVC remote storage"

# ----- STEP 6: Push Data to Remote -----
dvc push

# ----- STEP 7: Verify Remote Storage -----
# List contents of the remote to confirm upload
ls /tmp/dvc-remote

# ----- STEP 8: Modify Dataset (Version 2) -----
# Append a new record to student.csv
echo "66,Neha Joshi,93" >> data/student.csv

# Re-track the modified file with DVC
dvc add data/student.csv

# Commit the updated .dvc file
git add data/student.csv.dvc
git commit -m "Update student.csv dataset (Version 2)"

# Push new version to remote
dvc push

# ----- STEP 9: Switch Back to Version 1 -----
# Find the commit hash for Version 1
git log --oneline

# Checkout the Version 1 commit (replace <COMMIT_HASH_V1> with actual hash)
git checkout <COMMIT_HASH_V1>

# Restore the Version 1 dataset file
dvc checkout

# Verify the dataset is at Version 1
cat data/student.csv

# ----- STEP 10: Return to Latest Version -----
git checkout main
dvc checkout

# ----- STEP 11: Pull Data from Remote (Simulate Fresh Clone) -----
# In a fresh clone scenario, run:
dvc pull

# Verify data is restored
cat data/student.csv

# ============================================================
# End of DVC Assignment 1 Commands
# ============================================================
