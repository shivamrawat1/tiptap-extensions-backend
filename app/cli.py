import click
from flask.cli import with_appcontext
from app import db
from app.models.mcq_submission import MCQSubmission

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command) 