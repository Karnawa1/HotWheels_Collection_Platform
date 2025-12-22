"""
Flask CLI Commands for Database Management
Run with: flask db-migrate, flask db-status, etc.
"""
import click
from flask import current_app
from flask.cli import with_appcontext
from app.utils.db_manager import DatabaseManager
import logging

logger = logging.getLogger(__name__)

@click.group()
def db_commands():
    """Database management commands"""
    pass

@db_commands.command('migrate')
@with_appcontext
def migrate_command():
    """Run pending database migrations"""
    click.echo("🚀 Running database migrations...")

    database_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    if not database_url:
        click.echo("❌ Database URL not configured", err=True)
        return

    manager = DatabaseManager(database_url)
    success = manager.run_migrations()

    if success:
        click.echo("✅ Migrations completed successfully")
    else:
        click.echo("❌ Migrations failed", err=True)
        exit(1)

@db_commands.command('status')
@with_appcontext
def status_command():
    """Show migration status"""
    click.echo("📊 Database Migration Status\n")

    database_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    if not database_url:
        click.echo("❌ Database URL not configured", err=True)
        return

    manager = DatabaseManager(database_url)
    migrations = manager.get_migration_status()

    if migrations is None:
        click.echo("❌ Could not retrieve migration status", err=True)
        return

    if not migrations:
        click.echo("No migrations applied yet")
        return

    # Display table
    click.echo(f"{'Version':<40} {'Applied At':<25} {'Time (ms)':<12} {'Status'}")
    click.echo("-" * 90)

    for m in migrations:
        status = "✓" if m['success'] else "✗"
        click.echo(
            f"{m['version']:<40} "
            f"{str(m['applied_at']):<25} "
            f"{m['execution_time_ms'] or 'N/A':<12} "
            f"{status}"
        )

@db_commands.command('rollback')
@click.argument('version')
@with_appcontext
def rollback_command(version):
    """Rollback a specific migration (removes from tracking only)"""
    click.echo(f"⚠️  Rolling back migration: {version}")

    if not click.confirm('This will only remove the migration from tracking. Continue?'):
        click.echo("Cancelled")
        return

    database_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    if not database_url:
        click.echo("❌ Database URL not configured", err=True)
        return

    manager = DatabaseManager(database_url)
    success = manager.rollback_migration(version)

    if success:
        click.echo(f"✓ Migration {version} rolled back")
    else:
        click.echo(f"✗ Rollback failed", err=True)

@db_commands.command('reset')
@with_appcontext
def reset_command():
    """Reset migration tracking (DANGEROUS - removes all migration records)"""
    click.echo("⚠️  WARNING: This will remove all migration tracking!")
    click.echo("The database tables will remain, but migrations can be re-run.")

    if not click.confirm('Are you sure you want to continue?'):
        click.echo("Cancelled")
        return

    database_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    if not database_url:
        click.echo("❌ Database URL not configured", err=True)
        return

    import psycopg2
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS schema_migrations CASCADE")
        conn.commit()
        conn.close()
        click.echo("✓ Migration tracking reset")
    except Exception as e:
        click.echo(f"✗ Reset failed: {e}", err=True)

def register_commands(app):
    """Register all CLI commands with the Flask app"""
    app.cli.add_command(db_commands, name='db')