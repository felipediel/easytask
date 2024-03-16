"""Core app."""
__all__ = ["init_app"]

from flask import Flask

from .cryptography import bcrypt
from .database import db, migrate
from .error_handlers import register_error_handlers


def init_app(app: Flask, **_) -> None:
    """Register application."""
    # Set up error handlers
    register_error_handlers(app)

    # Set up database
    db.init_app(app)
    migrate.init_app(app, db)

    # Set up cryptography
    bcrypt.init_app(app)
