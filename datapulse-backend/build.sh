#!/bin/bash

echo "🐳 Building DataPulse Backend Docker Image..."

# Build the Docker image
docker build -t datapulse-backend .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo "🚀 To run the container:"
    echo "   docker run -p 8000:8000 datapulse-backend"
    echo ""
    echo "🌐 Or use docker-compose:"
    echo "   docker-compose up"
else
    echo "❌ Docker build failed!"
    exit 1
fi
