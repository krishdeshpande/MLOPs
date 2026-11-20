FROM python:3.11-slim

LABEL maintainer="Krish Deshpande | PRN: 12414049 | Roll: 61 | AIDS Div-C"
LABEL assignment="Assignment 8 - Prometheus + Grafana Monitoring"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Train the model at build time so it is ready at startup
RUN python train_model.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
