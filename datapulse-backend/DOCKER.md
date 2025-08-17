# 🐳 Docker Setup for DataPulse Backend

## 📋 Prerequisites

- Docker installed and running
- Docker Compose (optional, for easier orchestration)

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up --build

# Run in background
docker-compose up -d

# Stop the service
docker-compose down
```

### Option 2: Manual Docker Commands

```bash
# Build the image
./build.sh

# Run the container
./run.sh

# Or manually:
docker build -t datapulse-backend .
docker run -p 8000:8000 datapulse-backend
```

## 🔧 Docker Commands

### Build Image
```bash
docker build -t datapulse-backend .
```

### Run Container
```bash
docker run -p 8000:8000 datapulse-backend
```

### Run with Volume Mount (for data persistence)
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data datapulse-backend
```

### Stop Container
```bash
docker stop datapulse-backend
docker rm datapulse-backend
```

### View Logs
```bash
docker logs datapulse-backend
docker logs -f datapulse-backend  # Follow logs
```

## 📁 Volume Mounts

The Docker setup includes volume mounts for:
- **Data Directory**: `./data:/app/data` - Mount CSV files for analysis
- **Source Code**: Automatically copied during build

## 🌐 Access Points

- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/
- **Upload Endpoint**: http://localhost:8000/upload

## 🔍 Troubleshooting

### Container Won't Start
```bash
# Check container logs
docker logs datapulse-backend

# Check if port is already in use
lsof -i :8000
```

### Build Issues
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t datapulse-backend .
```

### Permission Issues
```bash
# Fix script permissions
chmod +x build.sh run.sh
```

## 📊 Production Considerations

For production deployment:

1. **Environment Variables**: Use `.env` files or Docker secrets
2. **Health Checks**: Built-in health check endpoint
3. **Logging**: Structured logging for monitoring
4. **Security**: Consider using non-root user in container
5. **Resource Limits**: Set memory and CPU limits

## 🎯 Next Steps

1. **Frontend Dockerization**: Containerize the React frontend
2. **Database Integration**: Add PostgreSQL/Redis containers
3. **Monitoring**: Add Prometheus/Grafana containers
4. **CI/CD**: Set up automated Docker builds
