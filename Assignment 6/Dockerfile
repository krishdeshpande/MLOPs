# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Train the model inside the container
RUN python train_model.py

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
