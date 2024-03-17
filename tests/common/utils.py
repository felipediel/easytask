"""Utils."""
from contextlib import contextmanager
from http import HTTPStatus
from pathlib import Path
from typing import IO, Generator


@contextmanager
def open_sample(
    filename, mode="r", encoding: str | None = None
) -> Generator[IO, None, None]:
    """Create sample directory function."""
    file_path = str(Path(__file__).parent / "samples" / filename)

    with open(file_path, mode=mode, encoding=encoding) as file:
        yield file


def assert_response_error(response, reason: str, status: HTTPStatus):
    """Check response error."""
    assert response.status_code == status, \
        f"Expected '{status}', received '{response.status_code}'"

    resp_data = response.json
    assert "error" in resp_data, "'error' not in response"

    error = resp_data["error"]
    assert "reason" in error, "'reason' not in error"
    assert error["reason"] == reason, \
        f"Expected '{reason}', received '{error['reason']}'"
