# 🚗 Hot Wheels Collector Platform

Full-stack application for Hot Wheels collectors to catalog, trade, and showcase their collections.

## 📁 Project Structure

```
├── hot-wheels-backend/     # Flask API (Python)
├── hot-wheels-frontend/    # Next.js Web App (TypeScript)
├── docs/                   # Platform documentation
│   └── ci-cd-pipeline.md   # CI/CD pipeline documentation
├── docker/                 # Docker configuration files
│   └── nginx/              # Nginx reverse proxy config
├── secrets/                # Production secrets (not committed)
├── .github/                # CI/CD workflows
│   └── workflows/
│       ├── ci.yml          # Continuous Integration
│       ├── cd.yml          # Continuous Deployment
│       └── pr-checks.yml   # Pull Request checks
├── docker-compose.yml      # Base Docker Compose config
├── docker-compose.override.yml  # Development overrides
└── docker-compose.prod.yml # Production overrides
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose v2+
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hot-wheels-platform
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the development environment**
   ```bash
   docker-compose up
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:5000
   - API Health: http://localhost:5000/health

### Production Deployment

1. **Create secrets files**
   ```bash
   cp secrets/postgres_password.txt.example secrets/postgres_password.txt
   cp secrets/jwt_secret.txt.example secrets/jwt_secret.txt
   cp secrets/mongo_password.txt.example secrets/mongo_password.txt
   # Edit each file with secure passwords
   ```

2. **Build and start production containers**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
   ```

3. **Access via Nginx**
   - Application: http://localhost (or https://your-domain.com)

## 🐳 Docker Services

| Service    | Port  | Description              |
|------------|-------|--------------------------|
| frontend   | 3000  | Next.js web application  |
| api        | 5000  | Flask REST API           |
| postgres   | 5432  | PostgreSQL database      |
| redis      | 6379  | Redis cache              |
| mongodb    | 27017 | MongoDB for media        |
| nginx      | 80/443| Reverse proxy (prod)     |

## 🔧 Useful Commands

### Development

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f frontend

# Rebuild containers
docker-compose up --build

# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v
```

### Production

```bash
# Start production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# View production logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Rolling restart
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --no-deps api
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --no-deps frontend
```

### Database

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U hotwheels_admin -d hotwheels_db

# Access MongoDB
docker-compose exec mongodb mongosh

# Access Redis
docker-compose exec redis redis-cli -a redis_secure_pass
```

## 🧪 Running Tests

### Backend Tests
```bash
cd hot-wheels-backend
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd hot-wheels-frontend
pnpm install
pnpm test           # Unit tests
pnpm test:e2e       # E2E tests
```

## 📦 CI/CD Pipeline

The project includes GitHub Actions workflows:

- **CI Pipeline** (`ci.yml`): Runs on push/PR
  - Backend: Lint, Test, Security Scan, Build Docker
  - Frontend: Lint, Type Check, Unit Tests, E2E Tests, Build Docker

- **CD Pipeline** (`cd.yml`): Deploys to staging/production
  - Triggered on successful CI on main branch
  - Manual deployment option available

- **PR Checks** (`pr-checks.yml`): Fast checks for PRs
  - Only runs checks for changed files
  - Validates Docker Compose configuration

## 🔒 Security

- All secrets should be stored in `.env` (local) or `secrets/` directory (production)
- Never commit `.env` or secret files to version control
- Use strong, unique passwords for all services
- Enable HTTPS in production via Nginx SSL configuration

## 📚 Documentation

- [CI/CD Pipeline](./docs/ci-cd-pipeline.md)
- [Backend API Documentation](./hot-wheels-backend/docs/README.md)
- [Frontend Architecture](./hot-wheels-frontend/ARCHITECTURE.md)
- [Contributing Guide](./hot-wheels-frontend/CONTRIBUTING.md)

## 📄 License

This project is private and proprietary.
