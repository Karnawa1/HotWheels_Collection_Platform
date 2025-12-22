-- ============================================
-- Create Application Roles
-- ============================================

\echo '👥 Creating application roles...'

-- Read-only role
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_read') THEN
        CREATE ROLE app_read WITH LOGIN PASSWORD 'read_pass_123';
    END IF;
END
$$;

-- Write role
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_write') THEN
        CREATE ROLE app_write WITH LOGIN PASSWORD 'write_pass_123';
    END IF;
END
$$;

-- Admin role
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_admin') THEN
        CREATE ROLE app_admin WITH LOGIN PASSWORD 'admin_pass_123';
    END IF;
END
$$;

\echo '✓ Application roles created'

-- Grant permissions (будут применены после создания таблиц)
GRANT CONNECT ON DATABASE hotwheels_db TO app_read, app_write, app_admin;
GRANT USAGE ON SCHEMA public TO app_read, app_write, app_admin;

\echo '✓ Basic permissions granted'
