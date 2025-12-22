-- ============================================
-- V006: Grant Permissions to Roles
-- Apply after all tables are created
-- ============================================

\echo '🔐 V006: Granting permissions to roles...'

-- Permissions for app_read role
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_read;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO app_read;

\echo '  ✓ app_read permissions granted'

-- Permissions for app_write role
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_write;
GRANT INSERT, UPDATE ON user_collections, wishlists, listings, transactions, reviews, user_sessions TO app_write;
GRANT DELETE ON user_sessions TO app_write; -- Only sessions can be deleted
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_write;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO app_write;

\echo '  ✓ app_write permissions granted'

-- Permissions for app_admin role
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_admin;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO app_admin;

\echo '  ✓ app_admin permissions granted'

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO app_write;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO app_admin;

\echo '  ✓ Default privileges set'

-- Revoke public schema permissions (security)
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

\echo '  ✓ Public schema secured'

\echo '✅ V006: All permissions granted successfully!'
