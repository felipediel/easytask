"""Management."""
from flask.cli import FlaskGroup

from easytask import create_app


cli = FlaskGroup(create_app=create_app)


if __name__ == "__main__":
    cli()
