"""
Database Migration Manager
Handles automatic execution of SQL migrations on startup
"""
import os
import psycopg2
from psycopg2 import sql
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database migrations and initialization"""

    def __init__(self, database_url):
        self.database_url = database_url
        self.migrations_dir = Path(__file__).parent.parent.parent / 'migrations'
        self.connection = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(self.database_url)
            self.connection.autocommit = False
            logger.info("✓ Database connection established")
            return True
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def create_migrations_table(self):
        """Create table to track applied migrations"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    execution_time_ms INTEGER,
                    success BOOLEAN DEFAULT TRUE
                )
            """)
            self.connection.commit()
            logger.info("✓ Migrations tracking table ready")
            return True
        except Exception as e:
            self.connection.rollback()
            logger.error(f"✗ Failed to create migrations table: {e}")
            return False

    def get_applied_migrations(self):
        """Get list of already applied migrations"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT version FROM schema_migrations ORDER BY version")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting applied migrations: {e}")
            return []

    def get_pending_migrations(self):
        """Get list of migrations that need to be applied"""
        if not self.migrations_dir.exists():
            logger.warning(f"Migrations directory not found: {self.migrations_dir}")
            return []

        # Get all .sql files starting with V
        all_migrations = sorted([
            f.name for f in self.migrations_dir.glob('V*.sql')
        ])

        applied = self.get_applied_migrations()
        pending = [m for m in all_migrations if m not in applied]

        logger.info(f"Found {len(all_migrations)} migrations, {len(applied)} applied, {len(pending)} pending")
        return pending

    def execute_migration(self, migration_file):
        """Execute a single migration file"""
        import time

        file_path = self.migrations_dir / migration_file
        logger.info(f"📦 Applying migration: {migration_file}")

        try:
            # Read migration file
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            # Remove psql-specific commands that don't work in psycopg2
            sql_content = sql_content.replace('\\echo', '--')

            # Execute migration
            cursor = self.connection.cursor()
            start_time = time.time()

            cursor.execute(sql_content)

            execution_time = int((time.time() - start_time) * 1000)

            # Record migration
            cursor.execute(
                "INSERT INTO schema_migrations (version, execution_time_ms) VALUES (%s, %s)",
                (migration_file, execution_time)
            )

            self.connection.commit()
            logger.info(f"✓ Migration {migration_file} applied successfully ({execution_time}ms)")
            return True

        except Exception as e:
            self.connection.rollback()
            logger.error(f"✗ Migration {migration_file} failed: {e}")

            # Record failed migration
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT INTO schema_migrations (version, success) VALUES (%s, %s)",
                    (migration_file, False)
                )
                self.connection.commit()
            except:
                pass

            return False

    def run_migrations(self):
        """Run all pending migrations"""
        logger.info("🚀 Starting database migration process...")

        if not self.connect():
            return False

        try:
            # Create migrations table
            if not self.create_migrations_table():
                return False

            # Get pending migrations
            pending = self.get_pending_migrations()

            if not pending:
                logger.info("✅ No pending migrations - database is up to date")
                return True

            # Apply each migration
            success_count = 0
            for migration in pending:
                if self.execute_migration(migration):
                    success_count += 1
                else:
                    logger.error(f"Migration process stopped due to failure in {migration}")
                    return False

            logger.info(f"✅ Successfully applied {success_count}/{len(pending)} migrations")
            return True

        finally:
            self.close()

    def rollback_migration(self, version):
        """Rollback a specific migration (manual operation)"""
        logger.warning(f"⚠️  Rolling back migration: {version}")

        if not self.connect():
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM schema_migrations WHERE version = %s",
                (version,)
            )
            self.connection.commit()
            logger.info(f"✓ Migration {version} rolled back from tracking")
            return True
        except Exception as e:
            self.connection.rollback()
            logger.error(f"✗ Rollback failed: {e}")
            return False
        finally:
            self.close()

    def get_migration_status(self):
        """Get status of all migrations"""
        if not self.connect():
            return None

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT version, applied_at, execution_time_ms, success 
                FROM schema_migrations 
                ORDER BY applied_at DESC
            """)

            migrations = []
            for row in cursor.fetchall():
                migrations.append({
                    'version': row[0],
                    'applied_at': row[1],
                    'execution_time_ms': row[2],
                    'success': row[3]
                })

            return migrations

        except Exception as e:
            logger.error(f"Error getting migration status: {e}")
            return None
        finally:
            self.close()