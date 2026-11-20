# Assignment 7: Docker Containerization

## Student Information

| Field       | Details            |
|-------------|--------------------|
| **Name**    | Krish Deshpande    |
| **PRN**     | 12414049           |
| **Roll No** | 61                 |
| **Class**   | AIDS Div-C         |

---

## Objective

Containerize a Machine Learning model (Iris LogisticRegression) using Docker and expose it as a REST API via Flask.

---

## Project Structure

```
Assignment 7/
├── app.py               # Flask REST API
├── train_model.py       # Model training script
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build instructions
├── docker_commands.sh   # Helper script with all Docker commands
└── README.md            # This file
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- `curl` (for testing endpoints)

---

## Docker Containerization Steps

### Step 1 — Build the Docker Image

```bash
docker build -t iris-classifier .
```

This command:
- Pulls `python:3.11-slim` as the base image
- Installs all Python dependencies from `requirements.txt`
- Copies project files into the container
- Runs `train_model.py` to train and save `model.joblib` inside the container

### Step 2 — Run the Container

```bash
docker run -d --name iris-api -p 5000:5000 iris-classifier
```

| Flag | Meaning |
|------|---------|
| `-d` | Detached (background) mode |
| `--name iris-api` | Assign a human-readable name |
| `-p 5000:5000` | Map host port 5000 → container port 5000 |

### Step 3 — Test the API with `curl`

**Welcome endpoint (GET /)**
```bash
curl http://localhost:5000/
```

**Predict endpoint (POST /predict)**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Expected response:
```json
{
  "prediction": 0,
  "class_name": "setosa"
}
```

### Step 4 — View Running Containers

```bash
docker ps
```

### Step 5 — View Container Logs

```bash
docker logs iris-api
```

### Step 6 — Stop and Remove the Container

```bash
docker stop iris-api
docker rm iris-api
```

### Step 7 — Remove the Image (optional)

```bash
docker rmi iris-classifier
```

---

## API Endpoints

| Method | Endpoint   | Description                          |
|--------|------------|--------------------------------------|
| GET    | `/`        | Welcome message and usage info       |
| POST   | `/predict` | Predict Iris class from 4 features   |

### POST /predict — Request Body

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

Features order: `[sepal_length, sepal_width, petal_length, petal_width]`

### POST /predict — Response

```json
{
  "prediction": 0,
  "class_name": "setosa"
}
```

| Class Index | Class Name  |
|-------------|-------------|
| 0           | setosa      |
| 1           | versicolor  |
| 2           | virginica   |

---

## Dockerfile Explanation

```dockerfile
FROM python:3.11-slim        # Lightweight Python base image
WORKDIR /app                 # Set working directory inside container
COPY requirements.txt .      # Copy deps first (layer caching)
RUN pip install --no-cache-dir -r requirements.txt  # Install deps
COPY . .                     # Copy all project files
RUN python train_model.py    # Train model at build time
EXPOSE 5000                  # Document the port
CMD ["python", "app.py"]     # Start Flask server
```

---

## Run All Commands at Once

A helper shell script is provided:

```bash
bash docker_commands.sh
```

This script builds the image, starts the container, runs all curl tests, then stops and removes the container.
