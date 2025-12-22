#!/bin/bash
# ===========================================
# Hot Wheels Platform - Container Entrypoint
# Handles startup, health checks, and graceful shutdown
# ===========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Graceful shutdown handler
shutdown_handler() {
    log_info "Received shutdown signal, gracefully stopping..."
    
    # Send SIGTERM to all child processes
    if [ -n "$APP_PID" ]; then
        kill -TERM "$APP_PID" 2>/dev/null || true
        
        # Wait for process to terminate (max 30 seconds)
        local count=0
        while kill -0 "$APP_PID" 2>/dev/null && [ $count -lt 30 ]; do
            sleep 1
            count=$((count + 1))
        done
        
        # Force kill if still running
        if kill -0 "$APP_PID" 2>/dev/null; then
            log_warning "Process did not terminate gracefully, forcing..."
            kill -KILL "$APP_PID" 2>/dev/null || true
        fi
    fi
    
    log_success "Shutdown complete"
    exit 0
}

# Register signal handlers
trap shutdown_handler SIGTERM SIGINT SIGQUIT

# Header
echo ""
echo "=========================================="
echo "🏎️  Hot Wheels Platform - Starting"
echo "=========================================="
echo ""

# Function to wait for PostgreSQL
wait_for_postgres() {
    log_info "Checking PostgreSQL connectivity..."

    local host="${DATABASE_HOST:-postgres}"
    local port="${DATABASE_PORT:-5432}"
    local user="${DATABASE_USER:-hotwheels_admin}"
    local db="${DATABASE_NAME:-hotwheels_db}"
    local max_attempts="${DB_CONNECT_RETRIES:-30}"
    local attempt=0

    until PGPASSWORD="$DATABASE_PASSWORD" psql -h "$host" -p "$port" -U "$user" -d "$db" -c 'SELECT 1;' > /dev/null 2>&1; do
        attempt=$((attempt + 1))

        if [ $attempt -ge $max_attempts ]; then
            log_error "PostgreSQL did not become ready in time (${max_attempts} attempts)"
            exit 1
        fi

        log_info "Attempt $attempt/$max_attempts - PostgreSQL not ready, waiting..."
        sleep 2
    done

    log_success "PostgreSQL is ready!"
}

# Function to wait for Redis (optional)
wait_for_redis() {
    log_info "Checking Redis connectivity..."
    
    local host="${REDIS_HOST:-redis}"
    local port="${REDIS_PORT:-6379}"
    local password="${REDIS_PASSWORD:-}"
    local max_attempts="${REDIS_CONNECT_RETRIES:-15}"
    local attempt=0
    
    # Build redis-cli command with password if provided
    local redis_cmd="redis-cli -h $host -p $port"
    if [ -n "$password" ]; then
        redis_cmd="$redis_cmd -a $password --no-auth-warning"
    fi
    
    until $redis_cmd ping 2>/dev/null | grep -q PONG; do
        attempt=$((attempt + 1))
        
        if [ $attempt -ge $max_attempts ]; then
            log_warning "Redis not ready (continuing without Redis)"
            return 1
        fi
        
        log_info "Attempt $attempt/$max_attempts - Redis not ready, waiting..."
        sleep 2
    done
    
    log_success "Redis is ready!"
    return 0
}

# Validate required environment variables
validate_environment() {
    log_info "Validating environment configuration..."
    
    local required_vars=(
        "DATABASE_HOST"
        "DATABASE_PORT"
        "DATABASE_USER"
        "DATABASE_NAME"
        "SECRET_KEY"
        "JWT_SECRET_KEY"
    )
    
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        log_warning "Missing environment variables: ${missing_vars[*]}"
        log_warning "Using default values where available"
    else
        log_success "All required environment variables are set"
    fi
}

# Main execution
main() {
    log_info "Environment: ${FLASK_ENV:-development}"
    log_info "Debug mode: ${DEBUG:-False}"
    log_info "API Port: ${API_PORT:-5000}"
    echo ""

    # Step 1: Validate environment
    log_info "Step 1/4: Validating environment..."
    validate_environment

    # Step 2: Wait for PostgreSQL
    log_info "Step 2/4: Checking database connectivity..."
    wait_for_postgres

    # Step 3: Wait for Redis (optional, non-blocking)
    log_info "Step 3/4: Checking Redis connectivity..."
    if [ "${REDIS_ENABLED:-true}" = "true" ]; then
        wait_for_redis || log_warning "Continuing without Redis cache"
    else
        log_info "Redis disabled, skipping..."
    fi

    # Step 4: Start application
    log_info "Step 4/4: Starting application..."
    echo ""

    if [ "${FLASK_ENV:-development}" = "production" ]; then
        log_info "Starting in PRODUCTION mode with Gunicorn"
        
        exec gunicorn \
            --bind "0.0.0.0:${API_PORT:-5000}" \
            --workers "${GUNICORN_WORKERS:-4}" \
            --threads "${GUNICORN_THREADS:-2}" \
            --timeout "${GUNICORN_TIMEOUT:-120}" \
            --graceful-timeout "${GUNICORN_GRACEFUL_TIMEOUT:-30}" \
            --keep-alive "${GUNICORN_KEEPALIVE:-5}" \
            --max-requests "${GUNICORN_MAX_REQUESTS:-1000}" \
            --max-requests-jitter "${GUNICORN_MAX_REQUESTS_JITTER:-100}" \
            --log-level "${LOG_LEVEL:-info}" \
            --access-logfile - \
            --error-logfile - \
            --capture-output \
            --enable-stdio-inheritance \
            "run:app" &
        
        APP_PID=$!
        wait $APP_PID
    else
        log_info "Starting in DEVELOPMENT mode with Flask"
        
        exec python run.py &
        
        APP_PID=$!
        wait $APP_PID
    fi
}

# Run main function
main "$@"
