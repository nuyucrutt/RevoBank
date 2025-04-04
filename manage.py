from flask import Flask
from flask_migrate import Migrate
from app import create_app
from src.models import db
import click
from flask.cli import with_appcontext

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("db-init")
def db_init():
    """Initialize database migrations"""
    from flask_migrate import init
    init()

@app.cli.command("db-migrate")
@click.argument('message')
def db_migrate(message):
    """Create migration scripts"""
    from flask_migrate import migrate as _migrate
    _migrate(message=message)

@app.cli.command("db-upgrade")
def db_upgrade():
    """Apply migrations to database"""
    from flask_migrate import upgrade
    upgrade()

if __name__ == '__main__':
    app.cli()
