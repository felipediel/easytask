"""Task app."""
__all__ = ["init_app"]

import posixpath

from flask import Flask

from .views import task_blueprint


def init_app(app: Flask, url_prefix="/") -> None:
    """Register application."""
    # Set up blueprints
    app.register_blueprint(
        task_blueprint, url_prefix=posixpath.join(url_prefix, "v1/tasks")
    )
