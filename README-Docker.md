# 🐳 DataPulse - Complete Docker Setup

## 🚀 Quick Start

### Prerequisites
- Docker installed on your system
- Docker Compose (included with Docker Desktop)

### 1. Start Both Services (Recommended)

```bash
# From the root directory (data_health/)
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

### 2. Individual Service Management

#### Backend Only
```bash
cd datapulse-backend
docker compose up -d
```

#### Frontend Only
```bash
cd datapulse-frontend
docker compose up -d
```

## 📊 Service Architecture

### Backend (FastAPI)
- **Port**: 8000
- **Base Image**: Python 3.10-slim
- **Framework**: FastAPI + Uvicorn
- **Features**: ML-powered data analysis, outlier detection, drift monitoring

### Frontend (React)
- **Port**: 3001
- **Base Image**: Node.js 18 (build) + Nginx Alpine (serve)
- **Framework**: React with Plotly.js charts
- **Features**: File upload, data visualization, interactive dashboards

## 🔧 Configuration

### Ports
- **Backend API**: `http://localhost:8000`
- **Frontend App**: `http://localhost:3001`
- **Backend Health**: `http://localhost:8000/`
- **Frontend Health**: `http://localhost:3001/`

### Volumes
- **Backend Data**: `./datapulse-backend/data:/app/data`
- **Frontend Build**: Built into container (no volume needed)

### Environment Variables
- **Backend**: `PYTHONUNBUFFERED=1`
- **Frontend**: None (static build)

## 🏗️ Docker Architecture

### Multi-Stage Frontend Build
1. **Build Stage**: Node.js 18 environment
   - Install dependencies
   - Build production bundle
2. **Serve Stage**: Nginx Alpine
   - Serve static files
   - Lightweight production server

### Backend Build
1. **Base**: Python 3.10-slim
2. **Dependencies**: Install from requirements.txt
3. **Source**: Copy application code
4. **Runtime**: Uvicorn ASGI server

## 🚀 Production Deployment

### Scaling
```bash
# Scale backend instances
docker compose up -d --scale backend=3

# Scale frontend instances (behind load balancer)
docker compose up -d --scale frontend=2
```

### Environment-Specific Configs
```bash
# Development
docker compose -f docker-compose.yml up -d

# Production
docker compose -f docker-compose.prod.yml up -d
```

## 🔍 Monitoring & Health Checks

### Backend Health
- **Endpoint**: `GET /`
- **Expected**: `{"status":"ok"}`
- **Check**: Every 30 seconds

### Frontend Health
- **Endpoint**: `GET /`
- **Expected**: HTML content
- **Check**: Every 30 seconds

### Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

## 🛠️ Development Workflow

### 1. Code Changes
```bash
# Backend changes require rebuild
docker compose build backend
docker compose up -d backend

# Frontend changes require rebuild
docker compose build frontend
docker compose up -d frontend
```

### 2. Hot Reload (Development)
```bash
# Run backend with volume mount for hot reload
docker run -v $(pwd)/datapulse-backend:/app -p 8000:8000 datapulse-backend

# Frontend: Use npm start in development
cd datapulse-frontend
npm start
```

## 🔒 Security Considerations

### Network Isolation
- Services communicate via Docker network
- No direct external access to backend
- Frontend serves as reverse proxy

### Resource Limits
```yaml
# Add to docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

## 📁 File Structure

```
data_health/
├── docker-compose.yml           # Main orchestration
├── datapulse-backend/
│   ├── Dockerfile              # Backend container
│   ├── docker-compose.yml      # Backend service
│   ├── requirements.txt        # Python dependencies
│   └── app/                    # FastAPI application
├── datapulse-frontend/
│   ├── Dockerfile              # Frontend container
│   ├── docker-compose.yml      # Frontend service
│   ├── package.json            # Node.js dependencies
│   └── src/                    # React application
└── README-Docker.md            # This file
```

## 🌐 Access URLs

### Development
- **Frontend**: `http://localhost:3000` (npm start)
- **Backend**: `http://localhost:8000` (uvicorn)

### Docker
- **Frontend**: `http://localhost:3001`
- **Backend**: `http://localhost:8000`

## 🎯 Next Steps

1. **Database Integration**: Add PostgreSQL/Redis containers
2. **Monitoring Stack**: Prometheus + Grafana
3. **CI/CD Pipeline**: GitHub Actions + Docker Hub
4. **Kubernetes**: Production orchestration
5. **SSL/TLS**: HTTPS with Let's Encrypt
6. **Load Balancing**: Traefik or HAProxy

## 🔍 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
lsof -i :8000
lsof -i :3001

# Use different ports
docker compose up -d -p 8001:8000 -p 3002:80
```

#### Build Failures
```bash
# Clean build cache
docker builder prune

# Rebuild without cache
docker compose build --no-cache
```

#### Container Won't Start
```bash
# Check logs
docker compose logs

# Check container status
docker compose ps
```

## 🎉 Success!

Your DataPulse application is now fully containerized with:
- ✅ **Backend**: FastAPI + ML algorithms
- ✅ **Frontend**: React + Plotly.js
- ✅ **Orchestration**: Docker Compose
- ✅ **Health Checks**: Automated monitoring
- ✅ **Production Ready**: Multi-stage builds

**Access your app at**: `http://localhost:3001` 🚀
