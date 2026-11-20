# Assignment 8: Prometheus + Grafana Monitoring for ML API

## Student Information
| Field | Details |
|-------|---------|
| **Name** | Krish Deshpande |
| **PRN** | 12414049 |
| **Roll No** | 61 |
| **Class** | AIDS Div-C |

---

## Objective
Implement a production-grade monitoring stack for an ML inference API using **Prometheus** for metrics collection and **Grafana** for visualization dashboards.

---

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Network                           │
│                                                                 │
│  ┌──────────────┐    scrape     ┌──────────────┐               │
│  │   ML API     │◄──────────────│  Prometheus  │               │
│  │  (FastAPI)   │  :8000/metrics│  :9090       │               │
│  │  Port: 8000  │               │              │               │
│  └──────────────┘               └──────┬───────┘               │
│                                        │ data source           │
│                                        ▼                        │
│                                 ┌──────────────┐               │
│                                 │   Grafana    │               │
│                                 │   :3000      │               │
│                                 └──────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### Components

| Service | Image / Build | Port | Purpose |
|---------|--------------|------|---------|
| **ml-api** | `./app` (custom build) | 8000 | FastAPI ML inference service |
| **prometheus** | `prom/prometheus` | 9090 | Time-series metrics DB & scraper |
| **grafana** | `grafana/grafana` | 3000 | Dashboard & visualization |

---

## Metrics Instrumented

| Metric Name | Type | Labels | Description |
|-------------|------|--------|-------------|
| `prediction_requests_total` | Counter | `status` (success/error) | Total prediction requests |
| `prediction_latency_seconds` | Histogram | — | Prediction endpoint latency |

---

## Project Structure

```
Assignment 8/
├── README.md
├── docker-compose.yml
├── test_requests.py
├── app/
│   ├── main.py              # FastAPI app with Prometheus metrics
│   ├── train_model.py       # Model training script
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Container build file
└── prometheus/
    └── prometheus.yml       # Prometheus scrape configuration
```

---

## Setup & Running

### 1. Train the Model (optional — Docker does this automatically)
```bash
cd app
pip install -r requirements.txt
python train_model.py
```

### 2. Start All Services
```bash
docker-compose up --build
```

### 3. Access Services
- **ML API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### 4. Run Test Requests
```bash
python test_requests.py
```

---

## Grafana Dashboard Setup

1. Open http://localhost:3000 → login with `admin` / `admin`
2. Go to **Connections → Data Sources → Add data source**
3. Select **Prometheus**, set URL: `http://prometheus:9090`
4. Click **Save & Test**
5. Create a new Dashboard with these PromQL queries:

| Panel Title | PromQL Query |
|-------------|--------------|
| Total Predictions | `prediction_requests_total` |
| Success Rate | `rate(prediction_requests_total{status="success"}[1m])` |
| Error Rate | `rate(prediction_requests_total{status="error"}[1m])` |
| Avg Latency (p95) | `histogram_quantile(0.95, rate(prediction_latency_seconds_bucket[5m]))` |
| Request Rate | `rate(prediction_requests_total[1m])` |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | Prometheus metrics |
| `POST` | `/predict` | Iris species prediction |

### Sample Predict Request
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

### Sample Response
```json
{
  "predicted_class": 0,
  "class_name": "setosa",
  "confidence": 0.98,
  "input_features": [5.1, 3.5, 1.4, 0.2]
}
```
