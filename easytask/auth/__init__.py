"""Authentication app."""
__all__ = ["init_app"]

import posixpath

from flask import Flask

from .token import jwt
from .views import auth_blueprint


def init_app(app: Flask, url_prefix="/") -> None:
    """Register application."""
    # Set up JWT Manager
    jwt.init_app(app)

    # Set up blueprints
    app.register_blueprint(
        auth_blueprint, url_prefix=posixpath.join(url_prefix, "v1/auth")
    )
