# Assignment 1: Dataset Versioning using DVC

## Student Information
| Field | Details |
|-------|---------|
| **Name** | Krish Deshpande |
| **PRN** | 12414049 |
| **Roll No** | 61 |
| **Class** | AIDS Div-C |

---

## Objective
To implement dataset versioning using **DVC (Data Version Control)** by tracking changes to a dataset (student marks) across multiple versions, enabling reproducibility and collaboration in ML/data projects.

---

## Tools & Technologies
- Git
- DVC (Data Version Control)
- Python
- Remote Storage (local/cloud)

---

## Steps Summary

1. **Initialize Git Repository**
   - Run `git init` to create a new Git repository in the project directory.

2. **Initialize DVC**
   - Run `dvc init` to set up DVC inside the Git repository.
   - Commit the DVC configuration files using `git commit`.

3. **Add Dataset to DVC**
   - Place the dataset (`data/student.csv`) in the project.
   - Run `dvc add data/student.csv` to start tracking the file with DVC.
   - This creates a `data/student.csv.dvc` metadata file and adds the actual CSV to `.gitignore`.

4. **Commit to Git**
   - Stage and commit the `.dvc` file and `.gitignore` using `git add` and `git commit`.

5. **Configure Remote Storage**
   - Set up a DVC remote (local folder or cloud bucket) using `dvc remote add`.

6. **Push Data to Remote**
   - Run `dvc push` to upload the dataset to the configured remote storage.

7. **Modify the Dataset (Version 2)**
   - Edit `data/student.csv` to add or update records.
   - Re-run `dvc add data/student.csv` to track the new version.
   - Commit the updated `.dvc` file to Git.
   - Run `dvc push` again.

8. **Switch Between Versions**
   - Use `git checkout <commit>` to switch to an older Git commit.
   - Run `dvc checkout` to restore the corresponding version of the dataset.

9. **Pull Data from Remote**
   - Run `dvc pull` to fetch and restore data from remote storage.

---

## Directory Structure
```
Assignment 1/
├── README.md
├── requirements.txt
├── dvc_commands.sh
└── data/
    └── student.csv
```
