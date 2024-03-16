"""Response."""
from http import HTTPStatus
from typing import Iterable, TypeVar

from pydantic import BaseModel

ResponseData = (
    BaseModel
    | list
    | dict
    | Iterable[bytes]
    | bytes
    | Iterable[str]
    | str
    | None
)
ResponseStatus = int | str | HTTPStatus

T = TypeVar("T", bound=ResponseData)


def success_response(
    data: T, status: ResponseStatus = HTTPStatus.OK
) -> tuple[T, HTTPStatus]:
    """Build success response."""
    status = HTTPStatus(status)
    return data, status


def error_response(
    reason: str | None = None,
    status: ResponseStatus = HTTPStatus.BAD_REQUEST,
    context: dict | None = None,
) -> tuple[ResponseData, HTTPStatus]:
    """Build error response."""
    status = HTTPStatus(status)

    if reason is None:
        reason = status.description

    resp_data = {"error": {"reason": reason}}

    if context:
        resp_data["error"]["context"] = context

    return resp_data, status
