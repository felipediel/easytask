"""Error handlers."""
from http import HTTPStatus

from flask_pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from flask import Flask, current_app

from .database import db
from .exceptions import APIException
from .response import error_response


def handle_api_exc(err: APIException):
    """Handle API exception."""
    return error_response(
        reason=err.message, status=err.status_code
    )


def handle_http_exc(err: HTTPException):
    """Handle HTTP exception"""
    status = HTTPStatus(err.code)
    if status == HTTPStatus.INTERNAL_SERVER_ERROR:
        current_app.logger.error(
            "An unhandled exception occurred", exc_info=True
        )
        db.session.rollback()

    description = err.description or status.description
    return error_response(reason=description, status=status)


def handle_validation_error(error: ValidationError):
    """Handle validation error."""
    status = HTTPStatus.BAD_REQUEST
    context = {}

    input_types = ["form_params", "body_params", "path_params", "query_params"]
    for input_type in input_types:
        if errors := getattr(error, input_type, None):
            context[input_type] = [
                {
                    "type": error["type"],
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "input": error["input"],
                }
                for error in errors
            ]

    return error_response(
        reason=status.description, context=context, status=status
    )


def handle_500(_: Exception):
    """Handle internal server error (500)."""
    current_app.logger.error("An unhandled exception occurred", exc_info=True)
    db.session.rollback()
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    return error_response(status=status)


def register_error_handlers(app: Flask):
    """Register error handlers."""
    app.register_error_handler(APIException, handle_api_exc)
    app.register_error_handler(HTTPException, handle_http_exc)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(Exception, handle_500)
