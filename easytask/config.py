"""Configuration."""
# pylint: disable=R0903
import datetime as dt

from decouple import config


class Config:
    """Base configuration."""

    # Flask
    DEBUG = False
    TESTING = False

    SECRET_KEY = config("FLASK_SECRET_KEY", default="")

    LOGGING = {
        "version": 1,
        "formatters": {"default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }},
        "handlers": {"wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default"
        }},
        "root": {
            "level": "INFO",
            "handlers": ["wsgi"]
        }
    }

    # Easytask
    INSTALLED_APPS = [
        "easytask.core",
        "easytask.auth",
        "easytask.tasks",
    ]

    # JWT Manager
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", default="")
    JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(hours=1)

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = config(
        "SQLALCHEMY_DATABASE_URI", default="sqlite://"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        "SQLALCHEMY_TRACK_MODIFICATIONS", default=False, cast=bool
    )

    # Flask-Pydantic
    FLASK_PYDANTIC_VALIDATION_ERROR_RAISE = True

    # Task service
    TASK_SERVICE_URL = config(
        "TASK_SERVICE_URL", default="https://jsonplaceholder.typicode.com"
    )
    TASK_SERVICE_TIMEOUT = config("TASK_SERVICE_TIMEOUT", default=30, cast=int)


class ProductionConfig(Config):
    """Production configuration."""


class DevelopmentConfig(Config):
    """Local configuration."""

    # Flask
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""

    # Flask
    DEBUG = True
    TESTING = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite://"


def get_config(environment: str) -> Config:
    """Get environment configuration."""
    config_map = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "testing": TestingConfig
    }
    try:
        return config_map[environment]()
    except KeyError as err:
        raise ValueError(f"Unknown environment: {environment}") from err
