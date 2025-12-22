# ===========================================
# Hot Wheels Platform - Flask API Dockerfile
# Multi-stage build with security hardening
# ===========================================

# ---------------------------------------------
# Stage 1: Builder - Install dependencies
# ---------------------------------------------
FROM python:3.11-slim-bookworm AS builder

# Set build-time arguments
ARG BUILDTIME_DEPS="gcc libpq-dev"

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ${BUILDTIME_DEPS} \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (layer caching optimization)
COPY requirements.txt .

# Install Python dependencies to user directory
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------------------------------------------
# Stage 2: Production - Final image
# ---------------------------------------------
FROM python:3.11-slim-bookworm AS production

# Labels for image metadata
LABEL maintainer="HotWheels Team <admin@hotwheels.com>"
LABEL version="1.0.0"
LABEL description="Hot Wheels Collector Platform - Flask API"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/home/appuser/.local/bin:$PATH" \
    APP_HOME=/app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/*

# Create non-root user for security
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Set working directory
WORKDIR ${APP_HOME}

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Create necessary directories with correct permissions
RUN mkdir -p ${APP_HOME}/logs ${APP_HOME}/uploads \
    && chown -R appuser:appgroup ${APP_HOME}

# Copy application code
COPY --chown=appuser:appgroup app/ ${APP_HOME}/app/
COPY --chown=appuser:appgroup migrations/ ${APP_HOME}/migrations/
COPY --chown=appuser:appgroup run.py ${APP_HOME}/
COPY --chown=appuser:appgroup entrypoint.sh ${APP_HOME}/

# Make entrypoint executable
RUN chmod +x ${APP_HOME}/entrypoint.sh

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 5000

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Use tini as init system for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start application
CMD ["./entrypoint.sh"]

# ---------------------------------------------
# Stage 3: Development - with debug tools
# ---------------------------------------------
FROM production AS development

# Switch back to root for installing dev tools
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    less \
    && rm -rf /var/lib/apt/lists/*

# Switch back to appuser
USER appuser

# Override for development
ENV FLASK_ENV=development \
    DEBUG=True
