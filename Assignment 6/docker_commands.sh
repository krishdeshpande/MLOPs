#!/bin/bash
# docker_commands.sh
# Docker build, run, test, and stop commands for the Iris Classification API
# Student: Krish Deshpande | PRN: 12414049 | Roll: 61 | Class: AIDS Div-C

IMAGE_NAME="iris-classifier"
CONTAINER_NAME="iris-api"
PORT=5000

echo "============================================================"
echo " Iris Classification API - Docker Commands"
echo "============================================================"

# ------------------------------------------------------------------
# 1. Build the Docker image
# ------------------------------------------------------------------
echo ""
echo "[1] Building Docker image: $IMAGE_NAME ..."
docker build -t $IMAGE_NAME .

# ------------------------------------------------------------------
# 2. Run the container (detached)
# ------------------------------------------------------------------
echo ""
echo "[2] Running container: $CONTAINER_NAME on port $PORT ..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:5000 \
  $IMAGE_NAME

echo "Container started. Waiting for the server to be ready..."
sleep 3

# ------------------------------------------------------------------
# 3. Test the endpoints with curl
# ------------------------------------------------------------------
echo ""
echo "[3] Testing GET / (welcome endpoint)..."
curl -s http://localhost:$PORT/ | python3 -m json.tool

echo ""
echo "[4] Testing POST /predict with sample features [5.1, 3.5, 1.4, 0.2] (expected: setosa)..."
curl -s -X POST http://localhost:$PORT/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}' | python3 -m json.tool

echo ""
echo "[5] Testing POST /predict with sample features [6.7, 3.0, 5.2, 2.3] (expected: virginica)..."
curl -s -X POST http://localhost:$PORT/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [6.7, 3.0, 5.2, 2.3]}' | python3 -m json.tool

echo ""
echo "[6] Testing POST /predict with invalid input (error handling)..."
curl -s -X POST http://localhost:$PORT/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0]}' | python3 -m json.tool

# ------------------------------------------------------------------
# 4. Show running containers
# ------------------------------------------------------------------
echo ""
echo "[7] Currently running containers:"
docker ps --filter name=$CONTAINER_NAME

# ------------------------------------------------------------------
# 5. Stop and remove the container
# ------------------------------------------------------------------
echo ""
echo "[8] Stopping and removing container: $CONTAINER_NAME ..."
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

echo ""
echo "Done. Container stopped and removed."
echo "To remove the image:  docker rmi $IMAGE_NAME"
