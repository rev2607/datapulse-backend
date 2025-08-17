#!/bin/bash

echo "🚀 Starting DataPulse Backend Container..."

# Check if image exists
if [[ "$(docker images -q datapulse-backend 2> /dev/null)" == "" ]]; then
    echo "📦 Building Docker image first..."
    ./build.sh
fi

# Run the container
echo "🌐 Starting container on http://localhost:8000"
docker run -p 8000:8000 \
    -v $(pwd)/data:/app/data \
    --name datapulse-backend \
    datapulse-backend
