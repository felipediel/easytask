"""Easytask app."""
__all__ = ["create_app"]

import importlib
import os
from logging.config import dictConfig

from flask import Flask

from easytask.core.exceptions import ImproperlyConfigured

from .config import get_config

__version__ = "1.0"


def create_app(env: str | None = None) -> Flask:
    """Create application."""
    app = Flask(__name__)

    # Set up app config
    if env is None:
        env = os.getenv("FLASK_ENV", default="development")

    app_config = get_config(env)
    app.config.from_object(app_config)

    # Set up logging
    dictConfig(app.config["LOGGING"])

    # Set up child apps
    installed_apps: list[str] = app.config["INSTALLED_APPS"]
    for app_name in installed_apps:
        load_child_app(app, app_name, url_prefix="/api")

    return app


def load_child_app(app: Flask, app_name: str, url_prefix="/") -> None:
    """Load child application."""
    try:
        app_module = importlib.import_module(app_name, package=__package__)
    except ImportError as err:
        raise ImproperlyConfigured(f"App not found: {app_name}") from err

    try:
        app_module.init_app(app, url_prefix=url_prefix)
    except AttributeError:
        app.logger.debug(
            "App '%s' does not have an 'init_app()' funtion", app_name
        )
    except TypeError as err:
        raise ImproperlyConfigured(
            f"The 'init_app()' function of the '{app_name}' app has invalid "
            "parameters"
        ) from err
