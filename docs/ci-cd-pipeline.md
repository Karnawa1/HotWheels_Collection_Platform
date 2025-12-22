# 🚀 CI/CD Pipeline Documentation

## Overview

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the **Hot Wheels Full-Stack Platform** (Backend API + Frontend Web Application). The pipeline automates code quality checks, testing, building, security scanning, and deployment processes for both services.

## 📊 Pipeline Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     HOT WHEELS FULL-STACK CI/CD PIPELINE                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   TRIGGER    │
└──────────────┘
 • Push to main
 • Push to develop
 • Pull Request
 • Manual (workflow_dispatch)
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
│  │               │                  │  │               │                                │
│  │ • Flake8      │                  │  │ • ESLint      │                                │
│  │ • Black       │                  │  │ • Prettier    │                                │
│  │ • isort       │                  │  │ • TypeScript  │                                │
│  └───────┬───────┘                  │  └───────┬───────┘                                │
│          │                          │          │                                        │
│          ▼                          │          ▼                                        │
│  ┌───────────────┐                  │  ┌───────────────┐  ┌───────────────┐             │
│  │   🧪 TEST     │                  │  │   🧪 TEST     │  │   🎭 E2E      │             │
│  │               │                  │  │               │  │               │             │
│  │ • pytest      │                  │  │ • Jest        │  │ • Playwright  │             │
│  │ • Coverage    │                  │  │ • Coverage    │  │ • Chromium    │             │
│  │ • Reports     │                  │  │ • Reports     │  │ • Reports     │             │
│  └───────┬───────┘                  │  └───────┬───────┘  └───────┬───────┘             │
│          │                          │          │                  │                     │
│          ▼                          │          └────────┬─────────┘                     │
│  ┌───────────────┐                  │                   ▼                               │
│  │  🔒 SECURITY  │                  │          ┌───────────────┐                        │
│  │               │                  │          │   🏗️ BUILD    │                        │
│  │ • pip-audit   │                  │          │               │                        │
│  │ • safety      │                  │          │ • pnpm build  │                        │
│  │ • bandit      │                  │          │ • Docker      │                        │
│  └───────┬───────┘                  │          │ • Multi-stage │                        │
│          │                          │          └───────┬───────┘                        │
│          ▼                          │                   │                               │
│  ┌───────────────┐                  │                   │                               │
│  │   🏗️ BUILD    │                  │                   │                               │
│  │               │                  │                   │                               │
│  │ • Docker      │                  │                   │                               │
│  │ • Multi-stage │                  │                   │                               │
│  │ • Push to     │                  │                   │                               │
│  │   Registry    │                  │                   │                               │
│  └───────┬───────┘                  │                   │                               │
│          │                          │                   │                               │
└──────────┼──────────────────────────┴───────────────────┼───────────────────────────────┘
           │                                              │
           ▼                                              ▼
     ┌─────────────────────────────────────────────────────────┐
     │              📦 DOCKER IMAGES (ghcr.io)                 │
     │  • hotwheels-api:latest                                 │
     │  • hotwheels-frontend:latest                            │
     └─────────────────────────────────────────────────────────┘
                                    │
                                    ▼
     ┌─────────────────────────────────────────────────────────────────────────────────┐
     │                              CD PIPELINE                                         │
     └─────────────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              ▼                                           ▼
       ┌───────────────┐                          ┌───────────────┐
       │ 🚀 STAGING    │                          │ 🚀 PRODUCTION │
       │               │                          │               │
       │ • Auto deploy │                          │ • Manual      │
       │ • API + FE    │                          │ • API + FE    │
       │ • Health      │                          │ • Health      │
       │   checks      │                          │   checks      │
       │               │                          │ • Rollback    │
       └───────────────┘                          └───────────────┘
                                                         │
                                                         ▼
                                                  ┌───────────────┐
                                                  │  📦 RELEASE   │
                                                  │               │
                                                  │ • Git Tag     │
                                                  │ • Changelog   │
                                                  │ • Artifacts   │
                                                  └───────────────┘
```

## 🛠️ Tools and Technologies

### Backend (Python/Flask)

| Category | Tool | Purpose |
|----------|------|---------|
| CI/CD Platform | GitHub Actions | Pipeline orchestration |
| Container Registry | GitHub Container Registry (ghcr.io) | Docker image storage |
| Code Linting | Flake8, Black, isort | Code style and formatting |
| Testing | pytest, pytest-cov | Unit tests and coverage |
| Security | pip-audit, safety, bandit | Vulnerability scanning |
| Containerization | Docker | Application packaging |

### Frontend (Next.js/TypeScript)

| Category | Tool | Purpose |
|----------|------|---------|
| CI/CD Platform | GitHub Actions | Pipeline orchestration |
| Container Registry | GitHub Container Registry (ghcr.io) | Docker image storage |
| Code Linting | ESLint | JavaScript/TypeScript linting |
| Formatting | Prettier | Code formatting |
| Type Checking | TypeScript | Static type analysis |
| Unit Testing | Jest | Unit tests and coverage |
| E2E Testing | Playwright | End-to-end browser tests |
| Package Manager | pnpm | Fast, efficient package management |
| Containerization | Docker | Application packaging |

### Shared Infrastructure

| Category | Tool | Purpose |
|----------|------|---------|
| Orchestration | Docker Compose | Multi-service deployment |
| Reverse Proxy | Nginx | Production routing and SSL |
| Database | PostgreSQL | Primary data store |
| Cache | Redis | Session and data caching |
| Media Storage | MongoDB | Image and media metadata |

## 📁 Pipeline Files Structure

```
.github/
└── workflows/
    ├── ci.yml          # Main CI pipeline
    ├── cd.yml          # Deployment pipeline
    └── pr-checks.yml   # Pull request validation
```

## 🔄 CI Pipeline Stages

### 🐍 Backend Pipeline

#### Stage 1: 🔍 Code Quality (Lint)

**Purpose:** Ensure consistent code style and catch syntax errors early.

**Tools:**
- **Flake8** - Python linting and style checking
- **Black** - Code formatting verification
- **isort** - Import sorting verification

**Configuration Files:**
- `.flake8` - Flake8 settings
- `pyproject.toml` - Black and isort settings

**What it checks:**
- Code style violations (PEP 8)
- Maximum line length (120 characters)
- Maximum cyclomatic complexity (10)
- Import organization
- Code formatting consistency

#### Stage 2: 🧪 Testing

**Purpose:** Verify application functionality and measure code coverage.

**Tools:**
- **pytest** - Test framework
- **pytest-cov** - Coverage measurement
- **pytest-flask** - Flask testing utilities

**Configuration:**
- Minimum coverage threshold: **60%**
- Test markers: `unit`, `integration`, `slow`

**Outputs:**
- Coverage report (HTML, XML)
- Test results (JUnit XML)
- Coverage summary in GitHub Actions

**Environment Variables:**
```yaml
FLASK_ENV: testing
SECRET_KEY: test-secret-key-for-ci
JWT_SECRET_KEY: test-jwt-secret-key-for-ci
DATABASE_URL: sqlite:///:memory:
```

#### Stage 3: 🔒 Security Scan

**Purpose:** Identify security vulnerabilities in dependencies and code.

**Tools:**
- **pip-audit** - Python package vulnerability scanner
- **safety** - Dependency security checker
- **bandit** - Static Application Security Testing (SAST)

**Outputs:**
- Security scan results in logs
- Summary in GitHub Actions

#### Stage 4: 🏗️ Build Docker Image

**Purpose:** Build and publish Docker images.

**Process:**
1. Set up Docker Buildx
2. Extract metadata (tags, labels)
3. Login to GitHub Container Registry
4. Build multi-stage Docker image
5. Push to registry (except for PRs)

**Image:** `ghcr.io/<owner>/hot-wheels-backend-api`

---

### ⚛️ Frontend Pipeline

#### Stage 1: 🔍 Code Quality (Lint)

**Purpose:** Ensure consistent code style and type safety.

**Tools:**
- **ESLint** - JavaScript/TypeScript linting
- **Prettier** - Code formatting verification
- **TypeScript** - Type checking

**Configuration Files:**
- `.eslintrc.json` - ESLint settings
- `.prettierrc` - Prettier settings
- `tsconfig.json` - TypeScript configuration

**What it checks:**
- ESLint rule violations
- Code formatting consistency
- TypeScript type errors
- Import/export issues

#### Stage 2: 🧪 Unit Testing

**Purpose:** Verify component functionality and measure code coverage.

**Tools:**
- **Jest** - Test framework
- **React Testing Library** - Component testing

**Configuration:**
- `jest.config.js` - Jest settings
- `jest.setup.js` - Test setup

**Outputs:**
- Coverage report
- Test results summary

#### Stage 3: 🎭 E2E Testing

**Purpose:** Verify end-to-end user flows in real browser.

**Tools:**
- **Playwright** - Browser automation
- **Chromium** - Test browser

**Configuration:**
- `playwright.config.ts` - Playwright settings

**Test Files:**
- `e2e/auth.spec.ts` - Authentication flows
- `e2e/collection.spec.ts` - Collection management

**Outputs:**
- Playwright HTML report
- Test artifacts (screenshots, videos on failure)

#### Stage 4: 🏗️ Build Docker Image

**Purpose:** Build and publish Docker images.

**Process:**
1. Set up Docker Buildx
2. Build Next.js application (`pnpm build`)
3. Create production Docker image
4. Push to registry (except for PRs)

**Image:** `ghcr.io/<owner>/hot-wheels-backend-frontend`

**Build Args:**
```yaml
NEXT_PUBLIC_API_URL: /api  # API endpoint for production
```

## 🚀 CD Pipeline Stages

### Environment: Staging

**Trigger:** Successful CI on `main` branch (automatic)

**Process:**
1. Prepare deployment artifacts
2. Create Docker Compose configuration
3. Generate deployment scripts
4. Upload as artifacts

### Environment: Production

**Trigger:** Manual workflow dispatch

**Process:**
1. Prepare deployment artifacts
2. Create Docker Compose configuration
3. Generate deployment and rollback scripts
4. Perform health checks
5. Automatic rollback on failure

### Release Creation

**Trigger:** Successful production deployment

**Process:**
1. Generate changelog from commits
2. Create GitHub release
3. Tag with version number
4. Attach deployment artifacts

## 🔐 Security Best Practices

### Secrets Management

All sensitive values are stored in **GitHub Secrets**:

| Secret | Purpose |
|--------|---------|
| `GITHUB_TOKEN` | Built-in, container registry access |
| `POSTGRES_PASSWORD` | Database password (for CD) |
| `REDIS_PASSWORD` | Cache password (for CD) |
| `JWT_SECRET_KEY` | JWT signing key (for CD) |
| `SECRET_KEY` | Flask secret key (for CD) |

### What's NOT in the Repository

- ❌ Passwords or API keys
- ❌ Database connection strings with credentials
- ❌ Private keys or certificates
- ❌ Environment-specific configuration

### Security Scans

1. **Dependency Vulnerabilities** - Checked on every pipeline run
2. **Code Security Issues** - Static analysis with Bandit
3. **Docker Image** - Multi-stage build, non-root user

## 📦 Artifacts

### Build Artifacts

| Artifact | Source | Retention | Description |
|----------|--------|-----------|-------------|
| `backend-coverage-report` | Backend | 14 days | HTML and XML coverage reports |
| `backend-test-results` | Backend | 14 days | JUnit XML test results |
| `frontend-coverage-report` | Frontend | 14 days | Jest coverage reports |
| `playwright-report` | Frontend | 14 days | E2E test HTML report |
| `staging-deployment-*` | CD | 7 days | Staging deployment scripts |
| `production-deployment-*` | CD | 30 days | Production deployment scripts |

### Docker Images

| Image | Registry | Tags |
|-------|----------|------|
| `hotwheels-api` | `ghcr.io/<owner>/hot-wheels-backend-api` | `latest`, `main`, `develop`, `<sha>` |
| `hotwheels-frontend` | `ghcr.io/<owner>/hot-wheels-backend-frontend` | `latest`, `main`, `develop`, `<sha>` |

**Image Tagging Strategy:**
- `latest` - Latest build from main branch
- `main` / `develop` - Branch-specific builds
- `pr-<number>` - Pull request builds
- `<sha>` - Commit SHA for traceability

## 🌍 Environments

### Development
- **Purpose:** Local development
- **Deployment:** Manual (`docker-compose up`)
- **Database:** Local PostgreSQL

### Staging
- **Purpose:** Pre-production testing
- **Deployment:** Automatic on main branch
- **URL:** `https://staging.hotwheels-platform.example.com`

### Production
- **Purpose:** Live environment
- **Deployment:** Manual trigger with approval
- **URL:** `https://hotwheels-platform.example.com`

## 🎯 Quality Gates

### Pull Request Requirements

1. ✅ All CI checks must pass
2. ✅ Code coverage ≥ 60%
3. ✅ No critical security vulnerabilities
4. ✅ Docker build successful

### Deployment Requirements

1. ✅ Successful CI pipeline
2. ✅ Health check passes
3. ✅ Manual approval (production only)

## 📋 How to Use

### Running CI Locally

#### Backend
```bash
cd hot-wheels-backend

# Install dev dependencies
pip install flake8 black isort pytest pytest-cov pytest-flask bandit

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

#### Frontend
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

### Manual Deployment Trigger

1. Go to **Actions** tab in GitHub
2. Select **CD Pipeline**
3. Click **Run workflow**
4. Select environment (`staging` or `production`)
5. Optionally specify version

### Downloading Deployment Artifacts

1. Go to completed workflow run
2. Scroll to **Artifacts** section
3. Download deployment package
4. Transfer to target server
5. Run `./deploy.sh`

### Rollback (Production)

```bash
# On production server
./rollback.sh
```

## 🔧 Customization

### Adding New Environments

1. Add environment in `cd.yml`
2. Create corresponding Docker Compose file
3. Add environment-specific secrets
4. Update deployment scripts

### Adjusting Coverage Threshold

Edit in `ci.yml`:
```yaml
--cov-fail-under=70  # Increase to 70%
```

### Adding New Security Scans

Add to security job in `ci.yml`:
```yaml
- name: Run new-tool
  run: |
    pip install new-tool
    new-tool scan app/
```

## 📊 Monitoring Pipeline

### GitHub Actions Dashboard

- View all workflow runs
- Check individual job logs
- Download artifacts
- Manually trigger workflows

### Notifications

Consider adding (optional enhancement):
- Slack notifications
- Email alerts
- Discord webhooks

## 🚨 Troubleshooting

### Pipeline Failures

#### Backend Issues
| Error | Solution |
|-------|----------|
| Lint fails | Run `black app/` and `isort app/` locally |
| Tests fail | Check test output, run locally with `pytest -v` |
| Build fails | Check Dockerfile syntax, dependencies |
| Security fails | Review vulnerability reports, update packages |

#### Frontend Issues
| Error | Solution |
|-------|----------|
| ESLint fails | Run `pnpm lint --fix` locally |
| Prettier fails | Run `pnpm format` locally |
| Type errors | Run `pnpm type-check` and fix TypeScript issues |
| Jest fails | Run `pnpm test` locally to debug |
| E2E fails | Check Playwright report, run `pnpm test:e2e --debug` |
| Build fails | Check Next.js build output, verify imports |

### Common Issues

1. **Cache miss** - First run takes longer, subsequent runs are faster
2. **Rate limits** - GitHub API limits, wait and retry
3. **Permission denied** - Check GITHUB_TOKEN permissions
4. **pnpm lockfile** - Run `pnpm install --frozen-lockfile` locally to verify
5. **Playwright browsers** - Run `pnpm exec playwright install` if browser tests fail

## 📚 References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [ESLint Documentation](https://eslint.org/docs/latest/)
- [pnpm Documentation](https://pnpm.io/)
