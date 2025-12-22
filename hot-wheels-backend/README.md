# 🏎️ Hot Wheels Collector Platform - Backend API

[![CI Pipeline](https://github.com/YOUR_USERNAME/hot-wheels-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/hot-wheels-backend/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/YOUR_USERNAME/hot-wheels-backend/actions/workflows/cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/hot-wheels-backend/actions/workflows/cd.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/hot-wheels-backend/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/hot-wheels-backend)

A Flask-based REST API for managing Hot Wheels collections, featuring PostgreSQL, Redis caching, and MongoDB for media storage.

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Quick Start](#-quick-start)
- [Container Documentation](#-container-documentation)
- [Environment Variables](#-environment-variables)
- [Development](#-development)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Production Deployment](#-production-deployment)
- [API Endpoints](#-api-endpoints)
- [Resource Requirements](#-resource-requirements)
- [Troubleshooting](#-troubleshooting)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Network                                │
│                     (hotwheels_network)                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                               │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │   │
│  │  │  PostgreSQL │    │    Redis    │    │   MongoDB   │      │   │
│  │  │   :5432     │    │    :6379    │    │   :27017    │      │   │
│  │  │  (Primary   │    │  (Session   │    │   (Media    │      │   │
│  │  │   Database) │    │   Cache)    │    │   Storage)  │      │   │
│  │  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │   │
│  │         │                  │                   │             │   │
│  │         └──────────────────┼───────────────────┘             │   │
│  │                            │                                  │   │
│  │                     ┌──────┴──────┐                          │   │
│  │                     │  Flask API  │                          │   │
│  │                     │   :5000     │                          │   │
│  │                     │  (Backend)  │                          │   │
│  │                     └─────────────┘                          │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Container Descriptions

| Container | Image | Purpose | Ports |
|-----------|-------|---------|-------|
| `hotwheels_api` | `hotwheels-api:1.0.0` | Flask REST API server | 5000 |
| `hotwheels_postgres` | `postgres:16-alpine` | Primary relational database | 5432 |
| `hotwheels_redis` | `redis:7-alpine` | Session/data caching | 6379 |
| `hotwheels_mongodb` | `mongo:7` | Media metadata storage | 27017 |

---

## 🚀 Quick Start

### Prerequisites

- Docker Engine 24.0+
- Docker Compose 2.20+
- 4GB RAM minimum
- 10GB disk space

### 1. Clone and Configure

```bash
# Clone repository
git clone <repository-url>
cd hot-wheels-backend

# Create environment file
cp .env.example .env

# Edit .env with your values (IMPORTANT: change passwords!)
```

### 2. Start Development Environment

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build

# View logs
docker-compose logs -f api
```

### 3. Verify Installation

```bash
# Check health endpoint
curl http://localhost:5000/health

# Expected response:
# {"service":"Hot Wheels API","status":"healthy","version":"1.0.0"}
```

---

## 🐳 Container Documentation

### Flask API (`hotwheels_api`)

**Purpose**: Main application server handling REST API requests.

| Property | Value |
|----------|-------|
| Base Image | `python:3.11-slim-bookworm` |
| Final Size | ~250MB |
| Internal Port | 5000 |
| External Port | ${API_PORT:-5000} |
| User | appuser (UID 1000) |
| Init System | tini |

**Volumes**:
- `./logs:/app/logs` - Application logs
- `./uploads:/app/uploads` - User uploaded files
- `./app:/app/app` (dev only) - Source code for hot reload

**Healthcheck**:
```bash
curl -f http://localhost:5000/health
# Interval: 30s, Timeout: 10s, Retries: 3
```

**Resource Limits**:
- Memory: 512MB (1GB in production)
- CPU: 0.5 cores (1.0 in production)

---

### PostgreSQL (`hotwheels_postgres`)

**Purpose**: Primary relational database for users, collections, and marketplace data.

| Property | Value |
|----------|-------|
| Image | `postgres:16-alpine` |
| Internal Port | 5432 |
| Data Volume | `postgres_data` |

**Healthcheck**:
```bash
pg_isready -U hotwheels_admin -d hotwheels_db
```

**Resource Limits**:
- Memory: 512MB (1GB in production)
- CPU: 0.5 cores (1.0 in production)

---

### Redis (`hotwheels_redis`)

**Purpose**: In-memory caching for sessions and frequently accessed data.

| Property | Value |
|----------|-------|
| Image | `redis:7-alpine` |
| Internal Port | 6379 |
| Data Volume | `redis_data` |
| Max Memory | 256MB |
| Eviction Policy | allkeys-lru |

**Healthcheck**:
```bash
redis-cli -a ${REDIS_PASSWORD} ping
```

**Resource Limits**:
- Memory: 256MB (512MB in production)
- CPU: 0.25 cores (0.5 in production)

---

### MongoDB (`hotwheels_mongodb`)

**Purpose**: NoSQL storage for media metadata and image references.

| Property | Value |
|----------|-------|
| Image | `mongo:7` |
| Internal Port | 27017 |
| Data Volume | `mongodb_data` |

**Healthcheck**:
```bash
mongosh --quiet --eval "db.runCommand('ping').ok"
```

**Resource Limits**:
- Memory: 512MB (1GB in production)
- CPU: 0.5 cores (1.0 in production)

---

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret for sessions | `your-secret-key-here` |
| `JWT_SECRET_KEY` | JWT token signing key | `jwt-secret-here` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `secure_password_123` |
| `MONGO_ROOT_PASSWORD` | MongoDB root password | `mongo_secure_pass` |

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Environment mode |
| `DEBUG` | `True` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `API_PORT` | `5000` | API external port |
| `AUTO_MIGRATE` | `True` | Run migrations on startup |

### Database Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_DB` | `hotwheels_db` | Database name |
| `POSTGRES_USER` | `hotwheels_admin` | Database user |
| `POSTGRES_PORT` | `5432` | External port |

### Cache Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_PASSWORD` | `redis_secure_pass` | Redis password |
| `REDIS_PORT` | `6379` | External port |

### JWT Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_ACCESS_TOKEN_EXPIRES` | `86400` | Token TTL (seconds) |
| `JWT_REFRESH_TOKEN_EXPIRES` | `2592000` | Refresh TTL (30 days) |

### Gunicorn Settings (Production)

| Variable | Default | Description |
|----------|---------|-------------|
| `GUNICORN_WORKERS` | `4` | Worker processes |
| `GUNICORN_THREADS` | `2` | Threads per worker |
| `GUNICORN_TIMEOUT` | `120` | Request timeout |

---

## 💻 Development

### File Structure

```
hot-wheels-backend/
├── app/                      # Application source code
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── middleware/          # Request processing
│   └── utils/               # Helper functions
├── docker/                   # Docker configurations
│   ├── postgres/            # PostgreSQL init scripts
│   ├── mongodb/             # MongoDB init scripts
│   └── redis/               # Redis configuration
├── migrations/              # Database migration files
├── tests/                   # Test files
├── logs/                    # Application logs
├── uploads/                 # User uploads
├── Dockerfile               # API container definition
├── docker-compose.yml       # Base compose file
├── docker-compose.override.yml  # Development overrides
├── docker-compose.prod.yml  # Production overrides
├── .env.example             # Environment template
└── .dockerignore            # Build exclusions
```

### Common Commands

```bash
# Start development environment
docker-compose up

# Rebuild after code changes
docker-compose up --build

# View API logs
docker-compose logs -f api

# Access API container shell
docker-compose exec api bash

# Run database migrations manually
docker-compose exec api flask db-migrate

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data!)
docker-compose down -v
```

### Hot Reload

In development mode, the `app/` directory is mounted as a volume. Code changes are automatically detected and the server restarts.

---

## 🔄 CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline using GitHub Actions.

### Pipeline Overview

```
Push/PR → Lint → Test → Build → Security Scan → Deploy
```

### CI Pipeline Features

| Stage | Description |
|-------|-------------|
| 🔍 **Lint** | Flake8, Black, isort code quality checks |
| 🧪 **Test** | pytest with coverage (minimum 60%) |
| 🏗️ **Build** | Multi-stage Docker build |
| 🔒 **Security** | pip-audit, safety, bandit scans |

### CD Pipeline Features

- **Staging**: Automatic deployment on `main` branch
- **Production**: Manual trigger with approval
- **Rollback**: Automatic rollback on failed health checks

### Running Locally

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 app/
black --check app/
isort --check-only app/

# Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Run security scan
bandit -r app/
pip-audit -r requirements.txt
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

For detailed CI/CD documentation, see [docs/ci-cd-pipeline.md](docs/ci-cd-pipeline.md).

---

## 🏭 Production Deployment

### Build Production Image

```bash
# Build with version tag
docker build -t hotwheels-api:1.0.0 --target production .

# Verify image size
docker images hotwheels-api:1.0.0
```

### Deploy to Production

```bash
# Use production compose file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Check status
docker-compose ps

# View production logs
docker-compose logs -f
```

### Production Checklist

- [ ] Change all default passwords in `.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Configure external SSL/TLS termination
- [ ] Set up log aggregation
- [ ] Configure backup for volumes
- [ ] Set appropriate resource limits
- [ ] Enable monitoring/alerting

---

## 📡 API Endpoints

### Health Check

```
GET /health
```

### Authentication

```
POST /api/v1/auth/register    # User registration
POST /api/v1/auth/login       # User login
POST /api/v1/auth/logout      # User logout
POST /api/v1/auth/refresh     # Refresh token
```

### Catalog

```
GET  /api/v1/catalog/models           # List car models
GET  /api/v1/catalog/models/{id}      # Get model details
GET  /api/v1/catalog/series           # List series
GET  /api/v1/catalog/manufacturers    # List manufacturers
```

### Collections

```
GET    /api/v1/collections            # List user collections
POST   /api/v1/collections            # Create collection
GET    /api/v1/collections/{id}       # Get collection
PUT    /api/v1/collections/{id}       # Update collection
DELETE /api/v1/collections/{id}       # Delete collection
```

### Marketplace

```
GET    /api/v1/marketplace/listings   # List marketplace items
POST   /api/v1/marketplace/listings   # Create listing
GET    /api/v1/marketplace/listings/{id}  # Get listing
```

---

## 💾 Resource Requirements

### Minimum Requirements

| Resource | Development | Production |
|----------|-------------|------------|
| RAM | 2 GB | 4 GB |
| CPU | 2 cores | 4 cores |
| Disk | 10 GB | 50 GB |

### Container Memory Allocation

| Container | Development | Production |
|-----------|-------------|------------|
| API | 1 GB | 1 GB |
| PostgreSQL | 512 MB | 1 GB |
| Redis | 256 MB | 512 MB |
| MongoDB | 512 MB | 1 GB |
| **Total** | **~2.3 GB** | **~3.5 GB** |

### Startup Times

| Metric | Typical Value |
|--------|---------------|
| Cold start (all containers) | 30-60 seconds |
| API ready | 15-30 seconds |
| Database ready | 10-15 seconds |

---

## 🔍 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs api

# Verify environment
docker-compose config

# Check resource usage
docker stats
```

### Database Connection Issues

```bash
# Test PostgreSQL connectivity
docker-compose exec postgres pg_isready -U hotwheels_admin

# Access PostgreSQL shell
docker-compose exec postgres psql -U hotwheels_admin -d hotwheels_db
```

### Reset Everything

```bash
# Stop and remove all containers, networks, volumes
docker-compose down -v

# Remove all images
docker rmi $(docker images -q hotwheels*)

# Fresh start
docker-compose up --build
```

### View Container Resource Usage

```bash
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

---

## 📜 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `docker-compose exec api pytest`
5. Submit a pull request

---

**Built with ❤️ for Hot Wheels collectors**
