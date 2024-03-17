"""Utils."""
from http import HTTPStatus


def map_gateway_http_status(status: int | str | HTTPStatus) -> HTTPStatus:
    """Map HTTP status from external service to gateway response."""
    status = HTTPStatus(status)
    status_map = {
        HTTPStatus.UNAUTHORIZED: HTTPStatus.UNAUTHORIZED,
        HTTPStatus.FORBIDDEN: HTTPStatus.FORBIDDEN,
        HTTPStatus.NOT_FOUND: HTTPStatus.NOT_FOUND,
        HTTPStatus.REQUEST_TIMEOUT: HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.UNPROCESSABLE_ENTITY: HTTPStatus.UNPROCESSABLE_ENTITY,
        HTTPStatus.TOO_MANY_REQUESTS: HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.SERVICE_UNAVAILABLE: HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.BAD_GATEWAY: HTTPStatus.BAD_GATEWAY,
        HTTPStatus.GATEWAY_TIMEOUT: HTTPStatus.GATEWAY_TIMEOUT,
    }

    try:
        return status_map[status]
    except KeyError:
        if status >= 500:
            return HTTPStatus.BAD_GATEWAY
        elif status >= 400:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        return status
