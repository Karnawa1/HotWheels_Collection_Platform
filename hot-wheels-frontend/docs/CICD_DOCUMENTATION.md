# CI/CD Documentation
## Hot Wheels Collector Platform

---

## Contents

1. [Overview](#1-overview)
2. [Pipeline Architecture](#2-pipeline-architecture)
   - 2.1 [Visual Diagram](#21-visual-diagram)
   - 2.2 [Pipeline Flow](#22-pipeline-flow)
3. [Technology Stack](#3-technology-stack)
4. [Repository Structure](#4-repository-structure)
   - 4.1 [GitHub Configuration Files](#41-github-configuration-files)
   - 4.2 [Docker Configuration Files](#42-docker-configuration-files)
5. [CI Pipeline](#5-ci-pipeline)
   - 5.1 [Triggers](#51-triggers)
   - 5.2 [Backend Pipeline](#52-backend-pipeline)
   - 5.3 [Frontend Pipeline](#53-frontend-pipeline)
   - 5.4 [Docker Build Stage](#54-docker-build-stage)
   - 5.5 [Pipeline Summary](#55-pipeline-summary)
6. [CD Pipeline](#6-cd-pipeline)
   - 6.1 [Triggers](#61-triggers)
   - 6.2 [Staging Deployment](#62-staging-deployment)
   - 6.3 [Production Deployment](#63-production-deployment)
   - 6.4 [Rollback Procedures](#64-rollback-procedures)
7. [PR Checks Workflow](#7-pr-checks-workflow)
   - 7.1 [Change Detection](#71-change-detection)
   - 7.2 [Quick Validation](#72-quick-validation)
8. [Container Registry](#8-container-registry)
   - 8.1 [Image Naming](#81-image-naming)
   - 8.2 [Tagging Strategy](#82-tagging-strategy)
   - 8.3 [Image Security](#83-image-security)
9. [Infrastructure as Code](#9-infrastructure-as-code)
   - 9.1 [Docker Compose Configurations](#91-docker-compose-configurations)
   - 9.2 [Nginx Reverse Proxy](#92-nginx-reverse-proxy)
   - 9.3 [Service Dependencies](#93-service-dependencies)
10. [Dependency Management](#10-dependency-management)
    - 10.1 [Dependabot Configuration](#101-dependabot-configuration)
    - 10.2 [Update Groups](#102-update-groups)
11. [Code Ownership](#11-code-ownership)
12. [Secrets Management](#12-secrets-management)
    - 12.1 [GitHub Secrets](#121-github-secrets)
    - 12.2 [Environment Variables](#122-environment-variables)
    - 12.3 [Docker Secrets](#123-docker-secrets)
13. [Environments](#13-environments)
    - 13.1 [Development](#131-development)
    - 13.2 [Staging](#132-staging)
    - 13.3 [Production](#133-production)
14. [Quality Gates](#14-quality-gates)
    - 14.1 [Pull Request Requirements](#141-pull-request-requirements)
    - 14.2 [Deployment Requirements](#142-deployment-requirements)
15. [Artifacts](#15-artifacts)
    - 15.1 [Build Artifacts](#151-build-artifacts)
    - 15.2 [Deployment Artifacts](#152-deployment-artifacts)
16. [Security Practices](#16-security-practices)
    - 16.1 [Backend Security Scanning](#161-backend-security-scanning)
    - 16.2 [Container Security](#162-container-security)
    - 16.3 [Production Hardening](#163-production-hardening)
17. [Monitoring & Observability](#17-monitoring--observability)
    - 17.1 [Health Checks](#171-health-checks)
    - 17.2 [Logging](#172-logging)
    - 17.3 [Pipeline Notifications](#173-pipeline-notifications)
18. [Local Development](#18-local-development)
    - 18.1 [Running CI Locally](#181-running-ci-locally)
    - 18.2 [Docker Development](#182-docker-development)
19. [Troubleshooting](#19-troubleshooting)
    - 19.1 [Common CI Failures](#191-common-ci-failures)
    - 19.2 [Common CD Failures](#192-common-cd-failures)
    - 19.3 [Docker Issues](#193-docker-issues)
20. [Best Practices](#20-best-practices)
21. [Conclusion](#21-conclusion)

---

## 1. Overview

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the **Hot Wheels Full-Stack Platform**. The pipeline automates:

- **Code Quality**: Linting, formatting, and static analysis
- **Testing**: Unit tests, integration tests, and E2E tests
- **Security Scanning**: Vulnerability detection in dependencies and code
- **Building**: Docker image creation and publishing
- **Deployment**: Automated staging and manual production releases

The platform consists of two main services:
- **Backend**: Python/Flask REST API
- **Frontend**: Next.js/TypeScript web application

Both services are containerized and deployed using Docker Compose with Nginx as a reverse proxy.

---

## 2. Pipeline Architecture

### 2.1 Visual Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     HOT WHEELS FULL-STACK CI/CD PIPELINE                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   TRIGGER    │
└──────────────┘
 • Push to main/develop
 • Pull Request
 • Feature branches
 • Manual dispatch
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CI PIPELINE                                           │
├─────────────────────────────────────┬───────────────────────────────────────────────────┤
│          🐍 BACKEND (Python/Flask)  │           ⚛️ FRONTEND (Next.js/TypeScript)         │
├─────────────────────────────────────┼───────────────────────────────────────────────────┤
│                                     │                                                   │
│  ┌───────────────┐                  │  ┌───────────────┐                                │
│  │   🔍 LINT     │                  │  │   🔍 LINT     │                                │
│  │ • Flake8      │                  │  │ • ESLint      │                                │
│  │ • Black       │                  │  │ • Prettier    │                                │
│  │ • isort       │                  │  │ • TypeScript  │                                │
│  └───────┬───────┘                  │  └───────┬───────┘                                │
│          │                          │          │                                        │
│          ▼                          │          ▼                                        │
│  ┌───────────────┐ ┌───────────────┐│  ┌───────────────┐  ┌───────────────┐             │
│  │   🧪 TEST     │ │  🔒 SECURITY  ││  │   🧪 TEST     │  │   🎭 E2E      │             │
│  │ • pytest      │ │  • pip-audit  ││  │ • Jest        │  │ • Playwright  │             │
│  │ • Coverage    │ │  • safety     ││  │ • Coverage    │  │ • Chromium    │             │
│  │ • 60% min     │ │  • bandit     ││  │               │  │               │             │
│  └───────┬───────┘ └───────┬───────┘│  └───────┬───────┘  └───────┬───────┘             │
│          │                 │        │          │                  │                     │
│          └────────┬────────┘        │          └────────┬─────────┘                     │
│                   ▼                 │                   ▼                               │
│          ┌───────────────┐          │          ┌───────────────┐                        │
│          │   🐳 BUILD    │          │          │   🐳 BUILD    │                        │
│          │ • Docker      │          │          │ • Docker      │                        │
│          │ • Multi-stage │          │          │ • Multi-stage │                        │
│          │ • Push GHCR   │          │          │ • Push GHCR   │                        │
│          └───────┬───────┘          │          └───────┬───────┘                        │
│                  │                  │                  │                                │
└──────────────────┼──────────────────┴──────────────────┼────────────────────────────────┘
                   │                                     │
                   ▼                                     ▼
     ┌─────────────────────────────────────────────────────────┐
     │              📦 DOCKER IMAGES (ghcr.io)                 │
     │  • ghcr.io/<owner>/hot-wheels-backend-api:latest        │
     │  • ghcr.io/<owner>/hot-wheels-backend-frontend:latest   │
     └─────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CD PIPELINE                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              ▼                                           ▼
       ┌───────────────┐                          ┌───────────────┐
       │ 🚀 STAGING    │                          │ 🚀 PRODUCTION │
       │               │                          │               │
       │ • Automatic   │                          │ • Manual      │
       │ • Health      │                          │ • Approval    │
       │   checks      │                          │ • Rollback    │
       └───────────────┘                          └───────────────┘
```

### 2.2 Pipeline Flow

| Stage | Trigger | Actions | Duration |
|-------|---------|---------|----------|
| **PR Checks** | Pull Request opened | Quick lint checks, change detection | ~2 min |
| **CI - Lint** | Push/PR | Code style, formatting, type checking | ~1-2 min |
| **CI - Test** | After Lint passes | Unit tests, coverage report | ~3-5 min |
| **CI - Security** | After Lint passes (backend) | Vulnerability scanning | ~2-3 min |
| **CI - E2E** | After Lint passes (frontend) | Browser tests with Playwright | ~5-8 min |
| **CI - Build** | After Tests pass | Docker image build and push | ~3-5 min |
| **CD - Staging** | CI succeeds on main | Auto-deploy to staging | ~2-3 min |
| **CD - Production** | Manual trigger | Deploy with approval | ~5-10 min |

---

## 3. Technology Stack

### CI/CD Platform
| Technology | Version | Purpose |
|------------|---------|---------|
| GitHub Actions | Latest | Workflow orchestration |
| GitHub Container Registry | Latest | Docker image storage |
| Docker Buildx | Latest | Multi-platform builds |

### Backend CI Tools
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11 | Runtime environment |
| Flake8 | Latest | Linting (PEP 8 compliance) |
| Black | Latest | Code formatting |
| isort | Latest | Import sorting |
| pytest | Latest | Test framework |
| pytest-cov | Latest | Coverage measurement |
| pytest-flask | Latest | Flask testing utilities |
| pip-audit | Latest | Dependency vulnerability scanning |
| safety | Latest | Security checker |
| bandit | Latest | Static Application Security Testing |

### Frontend CI Tools
| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 20 | Runtime environment |
| pnpm | 9 | Package manager |
| ESLint | 9.18+ | JavaScript/TypeScript linting |
| Prettier | 3.4+ | Code formatting |
| TypeScript | 5.x | Type checking |
| Jest | 30.2+ | Unit testing |
| Playwright | 1.57+ | E2E browser testing |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| Docker | Application containerization |
| Docker Compose | Multi-service orchestration |
| Nginx | Reverse proxy and load balancing |
| PostgreSQL | Primary database |
| Redis | Caching layer |
| MongoDB | Media metadata storage |

---

## 4. Repository Structure

### 4.1 GitHub Configuration Files

```
.github/
├── CODEOWNERS              # Automatic PR review assignment
├── dependabot.yml          # Automated dependency updates
└── workflows/
    ├── ci.yml              # Main CI pipeline (453 lines)
    ├── cd.yml              # Deployment pipeline (391 lines)
    └── pr-checks.yml       # Fast PR validation (171 lines)
```

### 4.2 Docker Configuration Files

```
/                           # Root level
├── docker-compose.yml           # Base configuration (293 lines)
├── docker-compose.override.yml  # Development overrides
├── docker-compose.prod.yml      # Production overrides (187 lines)
├── .env                         # Environment variables
├── .env.example                 # Environment template
│
├── docker/
│   └── nginx/
│       ├── nginx.conf           # Main Nginx configuration
│       ├── conf.d/              # Site configurations
│       └── ssl/                 # SSL certificates
│
├── hot-wheels-backend/
│   ├── Dockerfile               # Backend Docker build
│   └── docker/
│       ├── postgres/init-scripts/
│       ├── mongodb/init-scripts/
│       └── redis/redis.conf
│
├── hot-wheels-frontend/
│   └── Dockerfile               # Frontend Docker build (120 lines)
│
└── secrets/                     # Docker secrets (not committed)
    ├── jwt_secret.txt.example
    ├── mongo_password.txt.example
    └── postgres_password.txt.example
```

---

## 5. CI Pipeline

### 5.1 Triggers

The CI pipeline (`ci.yml`) runs on:

| Event | Branches | Description |
|-------|----------|-------------|
| `push` | `main`, `develop`, `feature/**` | Every commit to these branches |
| `pull_request` | `main`, `develop` | PR creation or update |
| `workflow_dispatch` | Any | Manual trigger from Actions tab |

**Environment Variables:**
```yaml
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
```

### 5.2 Backend Pipeline

#### Stage 1: 🔍 Lint (`backend-lint`)

**Purpose:** Ensure consistent code style and catch syntax errors early.

**Steps:**
1. Checkout code
2. Setup Python 3.11
3. Cache pip dependencies
4. Install linting tools
5. Run Flake8 (critical errors + style warnings)
6. Check imports with isort
7. Check formatting with Black

**Flake8 Configuration:**
```bash
# Critical errors (fail pipeline)
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Style warnings (non-blocking)
flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics
```

**Black Configuration:**
```bash
black --check --diff app/ --line-length 120
```

#### Stage 2: 🧪 Test (`backend-test`)

**Depends on:** `backend-lint`

**Purpose:** Verify application functionality and measure code coverage.

**Environment:**
```yaml
env:
  FLASK_ENV: testing
  SECRET_KEY: test-secret-key-for-ci
  JWT_SECRET_KEY: test-jwt-secret-key-for-ci
  DATABASE_URL: sqlite:///:memory:
```

**Coverage Requirements:**
- Minimum coverage: **60%**
- Coverage reports: HTML, XML, terminal

**Command:**
```bash
pytest tests/ \
  --cov=app \
  --cov-report=xml \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=60 \
  --junitxml=test-results.xml \
  -v
```

**Artifacts Produced:**
- `backend-coverage-report/` - HTML and XML coverage reports
- `backend-test-results/` - JUnit XML test results

#### Stage 3: 🔒 Security (`backend-security`)

**Depends on:** `backend-lint`

**Purpose:** Identify security vulnerabilities in dependencies and code.

**Tools:**
| Tool | Purpose | Behavior |
|------|---------|----------|
| pip-audit | Scan Python packages for CVEs | Continue on error |
| safety | Check dependencies against safety DB | Continue on error |
| bandit | Static analysis for security issues | Continue on error |

**Note:** Security checks use `continue-on-error: true` to avoid blocking deployments for minor issues while still generating reports.

### 5.3 Frontend Pipeline

#### Stage 1: 🔍 Lint (`frontend-lint`)

**Purpose:** Ensure consistent code style and type safety.

**Steps:**
1. Checkout code
2. Setup pnpm 9
3. Setup Node.js 20 with cache
4. Install dependencies (`pnpm install --frozen-lockfile`)
5. Run ESLint
6. Check Prettier formatting
7. TypeScript type checking

**Commands:**
```bash
pnpm lint           # ESLint
pnpm format:check   # Prettier
pnpm type-check     # TypeScript
```

#### Stage 2: 🧪 Unit Tests (`frontend-test`)

**Depends on:** `frontend-lint`

**Purpose:** Verify component functionality with Jest.

**Command:**
```bash
pnpm test:coverage
```

**Artifacts Produced:**
- `frontend-coverage-report/` - Jest coverage reports

#### Stage 3: 🎭 E2E Tests (`frontend-e2e`)

**Depends on:** `frontend-lint`

**Purpose:** Verify end-to-end user flows in real browser.

**Steps:**
1. Install dependencies
2. Install Playwright browsers (`chromium`)
3. Build application (`pnpm build`)
4. Run E2E tests

**Command:**
```bash
pnpm exec playwright install --with-deps chromium
pnpm build
pnpm test:e2e
```

**Artifacts Produced:**
- `playwright-report/` - HTML test report with screenshots

### 5.4 Docker Build Stage

#### Backend Build (`build-backend`)

**Depends on:** `backend-test`, `backend-security`

**Process:**
1. Setup Docker Buildx
2. Extract metadata (tags, labels)
3. Login to GitHub Container Registry
4. Build multi-stage Docker image
5. Push to registry (except for PRs)

**Image:** `ghcr.io/<owner>/hot-wheels-backend-api`

**Outputs:**
- `image_tag` - Docker image tags
- `image_digest` - Image digest for verification

#### Frontend Build (`build-frontend`)

**Depends on:** `frontend-test`, `frontend-e2e`

**Process:**
1. Setup Docker Buildx
2. Extract metadata (tags, labels)
3. Login to GitHub Container Registry
4. Build with API URL build arg
5. Push to registry (except for PRs)

**Image:** `ghcr.io/<owner>/hot-wheels-backend-frontend`

**Build Args:**
```yaml
build-args: |
  NEXT_PUBLIC_API_URL=${{ vars.NEXT_PUBLIC_API_URL || '/api' }}
```

### 5.5 Pipeline Summary

A final `summary` job runs after all jobs complete and generates a GitHub Actions summary:

```markdown
# 🚀 CI Pipeline Summary

## Backend
| Stage | Status |
|-------|--------|
| 🔍 Lint | success |
| 🧪 Test | success |
| 🔒 Security | success |
| 🐳 Build | success |

## Frontend
| Stage | Status |
|-------|--------|
| 🔍 Lint | success |
| 🧪 Unit Tests | success |
| 🎭 E2E Tests | success |
| 🐳 Build | success |

**Commit:** `abc123def`
**Branch:** `main`
**Actor:** @username
```

---

## 6. CD Pipeline

### 6.1 Triggers

The CD pipeline (`cd.yml`) runs on:

| Trigger | Condition | Result |
|---------|-----------|--------|
| `workflow_run` | CI Pipeline succeeds on `main` | Auto-deploy to staging |
| `workflow_dispatch` | Manual trigger | Deploy to selected environment |

**Manual Dispatch Inputs:**
```yaml
inputs:
  environment:
    description: 'Deployment environment'
    required: true
    default: 'staging'
    type: choice
    options:
      - staging
      - production
  version:
    description: 'Version/Tag to deploy (leave empty for latest)'
    required: false
    type: string
```

### 6.2 Staging Deployment

**Trigger:** Automatic after CI succeeds on `main`

**Environment:** `staging`
**URL:** `https://staging.hotwheels-platform.example.com`

**Process:**
1. Determine version (from input or git describe)
2. Determine Docker image tags
3. Create deployment artifacts:
   - `docker-compose.staging.yml`
   - `deploy.sh` script
4. Upload artifacts (retention: 7 days)

**Generated docker-compose.staging.yml:**
```yaml
version: '3.8'

services:
  api:
    image: ghcr.io/<owner>/hot-wheels-backend-api:latest
    container_name: hotwheels_api_staging
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: staging
      DEBUG: "False"
    env_file:
      - .env.staging
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - hotwheels_network

  frontend:
    image: ghcr.io/<owner>/hot-wheels-backend-frontend:latest
    container_name: hotwheels_frontend_staging
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
      NEXT_PUBLIC_API_URL: http://api:5000
    depends_on:
      - api
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - hotwheels_network

networks:
  hotwheels_network:
    driver: bridge
```

**Deployment Script (deploy.sh):**
```bash
#!/bin/bash
set -e

echo "🚀 Deploying Hot Wheels Platform to Staging..."

# Pull latest images
docker pull <api_image>
docker pull <frontend_image>

# Stop existing containers
docker-compose -f docker-compose.staging.yml down --remove-orphans || true

# Start new containers
docker-compose -f docker-compose.staging.yml up -d

# Wait for services to be healthy
sleep 15

# Verify deployment
if curl -sf http://localhost:5000/health > /dev/null; then
  echo "✅ API is healthy!"
else
  echo "❌ API health check failed!"
  exit 1
fi

if curl -sf http://localhost:3000 > /dev/null; then
  echo "✅ Frontend is healthy!"
else
  echo "❌ Frontend health check failed!"
  exit 1
fi

echo "✅ Deployment successful!"
```

### 6.3 Production Deployment

**Trigger:** Manual via workflow_dispatch

**Environment:** `production`
**URL:** `https://hotwheels-platform.example.com`

**Additional Features:**
- Nginx reverse proxy for SSL termination
- Resource limits enforced
- Rolling update strategy

**Production Services:**
```yaml
services:
  api:
    restart: always
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'

  frontend:
    restart: always
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
```

### 6.4 Rollback Procedures

**Automatic Rollback:**
If health checks fail during deployment, the script exits with error code 1, preventing container replacement.

**Manual Rollback:**
```bash
# On production server
./rollback.sh

# Or manually with Docker Compose
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml.backup up -d
```

**Version-based Rollback:**
```bash
# Pull specific version
docker pull ghcr.io/<owner>/hot-wheels-backend-api:v1.0.0
docker pull ghcr.io/<owner>/hot-wheels-backend-frontend:v1.0.0

# Update docker-compose and restart
docker-compose up -d
```

---

## 7. PR Checks Workflow

### 7.1 Change Detection

The PR checks workflow uses path filters to run only relevant checks:

```yaml
- name: 🔍 Detect file changes
  uses: dorny/paths-filter@v3
  with:
    filters: |
      backend:
        - 'hot-wheels-backend/**'
      frontend:
        - 'hot-wheels-frontend/**'
      docker:
        - 'docker-compose*.yml'
        - 'docker/**'
        - '.github/workflows/**'
```

### 7.2 Quick Validation

| Job | Condition | Checks |
|-----|-----------|--------|
| `backend-check` | Backend files changed | Flake8, Black, isort |
| `frontend-check` | Frontend files changed | ESLint, Prettier, TypeScript |
| `docker-check` | Docker files changed | docker-compose config validation |

**Docker Validation:**
```bash
docker-compose -f docker-compose.yml config --quiet
docker-compose -f docker-compose.yml -f docker-compose.prod.yml config --quiet
```

---

## 8. Container Registry

### 8.1 Image Naming

| Service | Image Name |
|---------|------------|
| Backend API | `ghcr.io/<owner>/hot-wheels-backend-api` |
| Frontend | `ghcr.io/<owner>/hot-wheels-backend-frontend` |

### 8.2 Tagging Strategy

| Tag | Source | Description |
|-----|--------|-------------|
| `latest` | `main` branch | Latest stable build |
| `main` | `main` branch | Main branch build |
| `develop` | `develop` branch | Development build |
| `pr-<number>` | Pull request | PR preview build |
| `<sha>` | Any push | Commit SHA for traceability |
| `feature-*` | Feature branches | Feature-specific build |

**Metadata Action Configuration:**
```yaml
- uses: docker/metadata-action@v5
  with:
    images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-api
    tags: |
      type=ref,event=branch
      type=ref,event=pr
      type=sha,prefix=
      type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}
```

### 8.3 Image Security

**Multi-stage Builds:**
Both Dockerfiles use multi-stage builds to minimize image size and attack surface:

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
# ...

# Stage 2: Build
FROM node:20-alpine AS builder
# ...

# Stage 3: Production (minimal image)
FROM node:20-alpine AS production
USER nextjs
# Only runtime files
```

**Non-root User:**
Production images run as non-root user:
- Backend: Custom app user
- Frontend: `nextjs:nodejs` (UID 1001)

---

## 9. Infrastructure as Code

### 9.1 Docker Compose Configurations

| File | Purpose | Usage |
|------|---------|-------|
| `docker-compose.yml` | Base configuration | Always included |
| `docker-compose.override.yml` | Development settings | Auto-loaded in dev |
| `docker-compose.prod.yml` | Production overrides | Explicit include |

**Production Usage:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Services Defined:**

| Service | Image | Ports (dev) | Ports (prod) |
|---------|-------|-------------|--------------|
| `postgres` | postgres:16-alpine | 5432:5432 | Internal only |
| `redis` | redis:7-alpine | 6379:6379 | Internal only |
| `mongodb` | mongo:7 | 27017:27017 | Internal only |
| `api` | hotwheels-api | 5000:5000 | Internal only |
| `frontend` | hotwheels-frontend | 3000:3000 | Internal only |
| `nginx` | nginx:alpine | 80, 443 | 80, 443 |

### 9.2 Nginx Reverse Proxy

**Configuration Highlights:**

```nginx
# Performance
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;

# Compression
gzip on;
gzip_comp_level 6;
gzip_types application/json text/css application/javascript;

# Security Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Rate Limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

# Upstreams
upstream api_backend {
    server api:5000;
    keepalive 32;
}

upstream frontend_backend {
    server frontend:3000;
    keepalive 32;
}
```

### 9.3 Service Dependencies

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  PostgreSQL │     │    Redis    │     │   MongoDB   │
│   (5432)    │     │   (6379)    │     │   (27017)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Flask API │
                    │   (5000)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Frontend  │
                    │   (3000)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Nginx    │
                    │  (80, 443)  │
                    └─────────────┘
```

**Health Check Dependencies:**
```yaml
api:
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy
    mongodb:
      condition: service_healthy

frontend:
  depends_on:
    api:
      condition: service_healthy
```

---

## 10. Dependency Management

### 10.1 Dependabot Configuration

Automated dependency updates are configured in `.github/dependabot.yml`:

| Ecosystem | Directory | Schedule | Limit |
|-----------|-----------|----------|-------|
| `pip` | `/hot-wheels-backend` | Weekly (Monday) | 5 PRs |
| `npm` | `/hot-wheels-frontend` | Weekly (Monday) | 5 PRs |
| `github-actions` | `/` | Weekly (Monday) | 5 PRs |
| `docker` | `/hot-wheels-backend` | Monthly | 5 PRs |
| `docker` | `/hot-wheels-frontend` | Monthly | 5 PRs |

### 10.2 Update Groups

Frontend dependencies are grouped to reduce PR noise:

| Group | Patterns | Update Types |
|-------|----------|--------------|
| `react-next` | `react*`, `next*`, `@next/*` | minor, patch |
| `radix` | `@radix-ui/*` | minor, patch |
| `testing` | `jest*`, `@jest/*`, `@testing-library/*`, `playwright*` | minor, patch |

**Commit Message Prefixes:**
- Backend: `chore(backend)`
- Frontend: `chore(frontend)`
- CI/CD: `chore(ci)`
- Docker: `chore(docker)`

---

## 11. Code Ownership

The `CODEOWNERS` file defines automatic PR reviewers:

```
# Default owners for everything
* @Karnawa1

# Backend specific
/hot-wheels-backend/ @Karnawa1

# Frontend specific
/hot-wheels-frontend/ @Karnawa1

# Infrastructure and DevOps
/docker/ @Karnawa1
/.github/ @Karnawa1
docker-compose*.yml @Karnawa1
```

**Effect:** Any PR touching these paths automatically requests review from the specified owners.

---

## 12. Secrets Management

### 12.1 GitHub Secrets

| Secret | Purpose | Used In |
|--------|---------|---------|
| `GITHUB_TOKEN` | Built-in token for registry access | CI, CD |
| `POSTGRES_PASSWORD` | Database password | CD only |
| `REDIS_PASSWORD` | Cache password | CD only |
| `JWT_SECRET_KEY` | JWT signing key | CD only |
| `SECRET_KEY` | Flask secret key | CD only |
| `MONGO_ROOT_PASSWORD` | MongoDB root password | CD only |

### 12.2 Environment Variables

**CI Environment (Test):**
```yaml
FLASK_ENV: testing
SECRET_KEY: test-secret-key-for-ci
JWT_SECRET_KEY: test-jwt-secret-key-for-ci
DATABASE_URL: sqlite:///:memory:
```

**Production Environment:**
```bash
# .env.production
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=WARNING
GUNICORN_WORKERS=4
GUNICORN_THREADS=2

# Secrets loaded from Docker secrets or environment
SECRET_KEY=${SECRET_KEY}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

### 12.3 Docker Secrets

For production, passwords can be loaded from Docker secrets:

```yaml
# docker-compose.prod.yml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
    secrets:
      - postgres_password

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
```

---

## 13. Environments

### 13.1 Development

| Property | Value |
|----------|-------|
| Purpose | Local development |
| Deployment | Manual (`docker-compose up`) |
| Database | Local PostgreSQL container |
| Debug | Enabled |
| Hot Reload | Enabled |

**Command:**
```bash
cd /project-root
docker-compose up -d
```

### 13.2 Staging

| Property | Value |
|----------|-------|
| Purpose | Pre-production testing |
| Deployment | Automatic on `main` branch |
| URL | `https://staging.hotwheels-platform.example.com` |
| Database | Shared staging database |
| Debug | Disabled |

**GitHub Environment:** `staging`

### 13.3 Production

| Property | Value |
|----------|-------|
| Purpose | Live user-facing environment |
| Deployment | Manual with approval |
| URL | `https://hotwheels-platform.example.com` |
| Database | Production database |
| Debug | Disabled |
| Monitoring | Enabled |

**GitHub Environment:** `production`

---

## 14. Quality Gates

### 14.1 Pull Request Requirements

| Requirement | Tool | Threshold |
|-------------|------|-----------|
| All CI checks pass | GitHub Actions | ✅ Required |
| Code coverage | pytest-cov | ≥ 60% |
| No critical security issues | bandit, pip-audit | Advisory |
| Docker build succeeds | Docker | ✅ Required |
| Type checks pass | TypeScript | ✅ Required |
| Linting passes | ESLint, Flake8 | ✅ Required |
| Formatting correct | Prettier, Black | ✅ Required |

### 14.2 Deployment Requirements

**Staging:**
- CI pipeline succeeds
- Images pushed to registry
- Health checks pass

**Production:**
- All staging requirements
- Manual approval required
- Deployment artifacts available
- Rollback script ready

---

## 15. Artifacts

### 15.1 Build Artifacts

| Artifact | Source | Retention | Description |
|----------|--------|-----------|-------------|
| `backend-coverage-report` | Backend CI | 14 days | HTML/XML coverage reports |
| `backend-test-results` | Backend CI | 14 days | JUnit XML test results |
| `frontend-coverage-report` | Frontend CI | 14 days | Jest coverage reports |
| `playwright-report` | Frontend CI | 14 days | E2E test HTML report |

### 15.2 Deployment Artifacts

| Artifact | Source | Retention | Contents |
|----------|--------|-----------|----------|
| `staging-deployment-<sha>` | CD | 7 days | compose file, deploy script |
| `production-deployment-<sha>` | CD | 30 days | compose file, deploy script, rollback script |

---

## 16. Security Practices

### 16.1 Backend Security Scanning

| Tool | Purpose | Checks |
|------|---------|--------|
| **pip-audit** | CVE scanning | Known vulnerabilities in packages |
| **safety** | Dependency check | Safety database comparison |
| **bandit** | SAST | Security issues in code |

**Bandit Severity:**
- `-ll` flag: Only report medium and high severity issues

### 16.2 Container Security

**Best Practices Implemented:**

| Practice | Implementation |
|----------|----------------|
| Non-root user | `USER nextjs` / `USER appuser` |
| Minimal base image | `alpine` variants |
| Multi-stage builds | Separate build and runtime stages |
| Health checks | All services have health endpoints |
| Read-only filesystem | Production volumes as `:ro` |

### 16.3 Production Hardening

**Nginx Security Headers:**
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

**Rate Limiting:**
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;
```

**Resource Limits:**
```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '1.0'
    reservations:
      memory: 512M
      cpus: '0.5'
```

---

## 17. Monitoring & Observability

### 17.1 Health Checks

| Service | Endpoint | Interval | Timeout |
|---------|----------|----------|---------|
| API | `http://localhost:5000/health` | 30s | 10s |
| Frontend | `http://localhost:3000` | 30s | 10s |
| PostgreSQL | `pg_isready` | 10s | 5s |
| Redis | `redis-cli ping` | 10s | 5s |
| MongoDB | `db.runCommand('ping')` | 10s | 5s |

### 17.2 Logging

**Production Logging Configuration:**
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "100m"
    max-file: "5"
```

**Log Levels by Environment:**
| Environment | Level |
|-------------|-------|
| Development | DEBUG |
| Staging | INFO |
| Production | WARNING |

### 17.3 Pipeline Notifications

**Built-in Notifications:**
- GitHub Actions summary
- PR status checks
- Deployment summaries

**Optional Integrations (can be added):**
- Slack webhooks
- Discord notifications
- Email alerts
- PagerDuty for critical failures

---

## 18. Local Development

### 18.1 Running CI Locally

**Backend:**
```bash
cd hot-wheels-backend

# Install dev dependencies
pip install flake8 black isort pytest pytest-cov pytest-flask bandit pip-audit safety

# Run linting
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
black --check app/ --line-length 120
isort --check-only app/

# Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=60

# Run security scan
bandit -r app/ -ll
pip-audit -r requirements.txt
```

**Frontend:**
```bash
cd hot-wheels-frontend

# Install dependencies
pnpm install

# Run linting
pnpm lint

# Check formatting
pnpm format:check

# Type check
pnpm type-check

# Run unit tests with coverage
pnpm test:coverage

# Run E2E tests
pnpm test:e2e
```

### 18.2 Docker Development

**Start All Services:**
```bash
# Development mode (with override)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Production Mode Locally:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Rebuild Specific Service:**
```bash
docker-compose up -d --build api
docker-compose up -d --build frontend
```

**Database Management:**
```bash
# Connect to PostgreSQL
docker exec -it hotwheels_postgres psql -U hotwheels_admin -d hotwheels_db

# Connect to Redis
docker exec -it hotwheels_redis redis-cli -a <password>

# Connect to MongoDB
docker exec -it hotwheels_mongodb mongosh
```

---

## 19. Troubleshooting

### 19.1 Common CI Failures

**Backend Issues:**

| Error | Cause | Solution |
|-------|-------|----------|
| Flake8 fails | Code style violations | Run `flake8 app/` locally, fix issues |
| Black fails | Formatting issues | Run `black app/` locally |
| isort fails | Import order | Run `isort app/` locally |
| Tests fail | Test failures | Run `pytest -v` locally, check logs |
| Coverage < 60% | Insufficient tests | Add more test cases |
| Security scan fails | Vulnerable packages | Update dependencies |

**Frontend Issues:**

| Error | Cause | Solution |
|-------|-------|----------|
| ESLint fails | Linting errors | Run `pnpm lint --fix` locally |
| Prettier fails | Formatting issues | Run `pnpm format` locally |
| TypeScript fails | Type errors | Run `pnpm type-check`, fix errors |
| Jest fails | Test failures | Run `pnpm test` locally |
| E2E fails | Browser test failure | Check Playwright report |
| Build fails | Next.js build error | Run `pnpm build` locally |
| pnpm lockfile | Lockfile mismatch | Run `pnpm install --frozen-lockfile` |

### 19.2 Common CD Failures

| Error | Cause | Solution |
|-------|-------|----------|
| Image pull fails | Registry auth | Check GITHUB_TOKEN permissions |
| Health check fails | Service not ready | Increase start period, check logs |
| Port conflict | Port in use | Stop conflicting services |
| Memory limit | OOM killed | Increase resource limits |
| Network error | DNS resolution | Check Docker network config |

### 19.3 Docker Issues

| Error | Cause | Solution |
|-------|-------|----------|
| Build cache miss | First build | Normal, subsequent builds faster |
| Layer caching | Dependencies changed | Expected, rebuild required |
| Permission denied | File ownership | Check USER in Dockerfile |
| Volume mount fails | Path doesn't exist | Create directory first |
| Compose config invalid | YAML syntax | Run `docker-compose config` |

---

## 20. Best Practices

### CI/CD Best Practices

| Practice | Implementation |
|----------|----------------|
| Fast feedback | PR checks run in ~2 minutes |
| Parallel execution | Backend and frontend run in parallel |
| Fail fast | Lint before test, test before build |
| Immutable artifacts | Docker images tagged with SHA |
| Environment parity | Same Docker images in all envs |
| Infrastructure as Code | All config in version control |

### Security Best Practices

| Practice | Implementation |
|----------|----------------|
| Secrets in GitHub Secrets | No credentials in code |
| Non-root containers | Production images run as non-root |
| Minimal images | Alpine base, multi-stage builds |
| Dependency scanning | Automated with Dependabot |
| Security gates | bandit, pip-audit, safety scans |

### Deployment Best Practices

| Practice | Implementation |
|----------|----------------|
| Health checks | All services have health endpoints |
| Rolling updates | One service at a time in production |
| Rollback capability | Previous version always available |
| Resource limits | Memory and CPU limits enforced |
| Logging | Structured JSON logs with rotation |

---

## 21. Conclusion

The Hot Wheels Platform CI/CD pipeline provides a robust, automated workflow for continuous integration and deployment of both backend and frontend services.

### Key Achievements

| Area | Implementation |
|------|----------------|
| **Automation** | Full CI/CD from commit to deployment |
| **Quality** | Linting, testing, and coverage gates |
| **Security** | Vulnerability scanning, non-root containers |
| **Speed** | Parallel jobs, caching, fast PR checks |
| **Reliability** | Health checks, rollback procedures |
| **Observability** | Artifacts, summaries, logging |
| **Scalability** | Docker Compose, resource limits |

### Pipeline Summary

| Metric | Value |
|--------|-------|
| Total CI Time | ~10-15 minutes |
| PR Check Time | ~2-3 minutes |
| Deployment Time | ~2-5 minutes |
| Coverage Threshold | 60% |
| Artifact Retention | 7-30 days |
| Image Tags | latest, branch, sha |

### Future Enhancements

- [ ] Add Slack/Discord notifications
- [ ] Implement blue-green deployments
- [ ] Add performance testing stage
- [ ] Implement semantic versioning automation
- [ ] Add Kubernetes deployment option
- [ ] Implement feature flag integration

---

**Document Version**: 1.0.0  
**Last Updated**: December 2025  
**Maintained By**: Hot Wheels Platform DevOps Team

---

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [pytest Documentation](https://docs.pytest.org/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [ESLint Documentation](https://eslint.org/docs/latest/)
- [pnpm Documentation](https://pnpm.io/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
