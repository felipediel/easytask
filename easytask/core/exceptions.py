"""Exceptions."""
from http import HTTPStatus


class APIException(Exception):
    """API exception."""

    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    default_message = HTTPStatus.INTERNAL_SERVER_ERROR.description
    default_code = HTTPStatus.INTERNAL_SERVER_ERROR.name

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        payload: list | dict | None = None,
    ):
        """Initialize the exception."""
        if message is None:
            message = self.default_message

        if code is None:
            code = self.default_code

        self.message = message
        self.code = code
        self.payload = payload


class BadRequestError(APIException):
    """Bad request error."""

    status_code = HTTPStatus.BAD_REQUEST
    default_message = HTTPStatus.BAD_REQUEST.description
    default_code = HTTPStatus.BAD_REQUEST.name


class NotFoundError(APIException):
    """Bad request error."""

    status_code = HTTPStatus.NOT_FOUND
    default_message = HTTPStatus.NOT_FOUND.description
    default_code = HTTPStatus.NOT_FOUND.name


class UnauthorizedError(APIException):
    """Unauthorized error."""

    status_code = HTTPStatus.UNAUTHORIZED
    default_message = HTTPStatus.UNAUTHORIZED.description
    default_code = HTTPStatus.UNAUTHORIZED.name


class InternalServerError(APIException):
    """Internal server error."""


class ImproperlyConfigured(InternalServerError):
    """Improperly configured error."""


class ServiceUnavailableError(APIException):
    """Service unavailable error."""

    status_code = HTTPStatus.SERVICE_UNAVAILABLE
    default_message = HTTPStatus.SERVICE_UNAVAILABLE.description
    default_code = HTTPStatus.SERVICE_UNAVAILABLE.name


class BadGatewayError(APIException):
    """Bad gateway error."""

    status_code = HTTPStatus.BAD_GATEWAY
    default_message = HTTPStatus.BAD_GATEWAY.description
    default_code = HTTPStatus.BAD_GATEWAY.name


class GatewayTimeoutError(APIException):
    """Gateway timeout error."""

    status_code = HTTPStatus.GATEWAY_TIMEOUT
    default_message = HTTPStatus.GATEWAY_TIMEOUT.description
    default_code = HTTPStatus.GATEWAY_TIMEOUT.name
