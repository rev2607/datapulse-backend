# 🐳 DataPulse Backend - Docker Deployment

## 🚀 Quick Start with Docker

### Prerequisites
- Docker installed on your system
- Docker Compose (included with Docker Desktop)

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Start the backend service
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f backend

# Stop the service
docker compose down
```

### 2. Manual Docker Commands

```bash
# Build the image
docker build -t datapulse-backend .

# Run the container
docker run -d -p 8000:8000 --name datapulse-backend datapulse-backend

# Check container status
docker ps

# View logs
docker logs datapulse-backend

# Stop and remove container
docker stop datapulse-backend
docker rm datapulse-backend
```

## 📊 Testing the Containerized Backend

### Health Check
```bash
curl http://localhost:8000/
# Expected: {"status":"ok"}
```

### Upload Test
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@data2.csv"
```

## 🔧 Configuration

### Environment Variables
- `PYTHONUNBUFFERED=1`: Ensures Python output is not buffered

### Ports
- **Host**: 8000
- **Container**: 8000

### Volumes
- `./data:/app/data`: Mounts local data directory for CSV files

## 🏗️ Docker Architecture

### Base Image
- **Python 3.10-slim**: Lightweight Python runtime
- **Size**: ~40MB base + dependencies

### Layers
1. **Base Python**: Official Python slim image
2. **Dependencies**: Install requirements.txt
3. **Source Code**: Copy application files
4. **Runtime**: Uvicorn ASGI server

### Health Checks
- **Endpoint**: `GET /`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

## 🚀 Production Considerations

### Security
- Run as non-root user (add to Dockerfile)
- Use specific Python version tags
- Scan for vulnerabilities: `docker scout quickview`

### Performance
- Multi-stage builds for smaller images
- Alpine Linux for minimal footprint
- Gunicorn + Uvicorn workers for production

### Monitoring
- Health check endpoint
- Log aggregation
- Metrics collection

## 🔍 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Stop conflicting service or use different port
docker run -p 8001:8000 datapulse-backend
```

#### Container Won't Start
```bash
# Check logs
docker compose logs backend

# Check container status
docker compose ps
```

#### Build Failures
```bash
# Clean build cache
docker builder prune

# Rebuild without cache
docker build --no-cache -t datapulse-backend .
```

## 📁 File Structure

```
datapulse-backend/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Service orchestration
├── .dockerignore          # Build exclusions
├── requirements.txt        # Python dependencies
├── app/                   # Application code
│   ├── main.py           # FastAPI app
│   └── utils.py          # Analysis functions
└── data/                  # CSV files (mounted volume)
```

## 🌐 Integration with Frontend

The containerized backend is configured with CORS to allow connections from:
- `http://localhost:3000` (React development server)
- Update `docker-compose.yml` for production URLs

## 🎯 Next Steps

1. **Frontend Containerization**: Create Docker setup for React app
2. **Database Integration**: Add PostgreSQL/Redis containers
3. **CI/CD Pipeline**: Automated testing and deployment
4. **Kubernetes**: Production orchestration
5. **Monitoring**: Prometheus + Grafana setup
