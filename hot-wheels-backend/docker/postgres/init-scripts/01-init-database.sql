-- ============================================
-- PostgreSQL Initialization Script
-- Hot Wheels Platform Database
-- ============================================

\echo '🚀 Initializing Hot Wheels Platform Database...'

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For composite indexes

\echo '✓ Extensions created'

-- Create schemas (optional - for better organization)
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS marketplace;
CREATE SCHEMA IF NOT EXISTS analytics;

\echo '✓ Schemas created'

-- Grant usage on schemas
GRANT USAGE ON SCHEMA core TO PUBLIC;
GRANT USAGE ON SCHEMA marketplace TO PUBLIC;
GRANT USAGE ON SCHEMA analytics TO PUBLIC;

\echo '✓ Database initialized successfully!'
