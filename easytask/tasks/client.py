"""API Client."""
import posixpath
import uuid
from urllib.parse import urlparse

import requests

from flask import current_app


class APIClient:
    """API client."""

    def __init__(self, api_url: str) -> None:
        """Initialize client."""
        self.api_url = api_url

    def build_url(self, *path: str) -> str:
        """Build URL."""
        return posixpath.join(self.api_url, *path)

    def send_request(
        self, method: str, url: str, **kwargs
    ) -> requests.Response:
        """Send HTTP request."""
        request = requests.PreparedRequest()
        session = requests.Session()

        request.prepare(method, url, **kwargs)
        request_id = str(uuid.uuid4())
        parsed_req_url = urlparse(request.url)
        timeout = current_app.config["TASK_SERVICE_TIMEOUT"]

        current_app.logger.info(
            "Sending HTTP request to <%s://%s>: '%s %s' (rid=%r)",
            parsed_req_url.scheme,
            parsed_req_url.netloc,
            request.method,
            parsed_req_url.path,
            request_id,
        )

        try:
            resp = session.send(request, timeout=timeout)
        except requests.RequestException as err:
            current_app.logger.error(
                "HTTP request failed: %s (rid=%r)", err, request_id
            )
            raise
        finally:
            session.close()

        parsed_resp_url = urlparse(resp.url)

        current_app.logger.info(
            "HTTP response received from <%s://%s>: %s %s (rid=%r)",
            parsed_resp_url.scheme,
            parsed_resp_url.netloc,
            resp.status_code,
            resp.content,
            request_id,
        )

        return resp


class TaskAPIClient(APIClient):
    """Task API client."""

    def get_task_list(self, params: dict | None = None) -> requests.Response:
        """Get task list."""
        url = self.build_url("todos")
        resp = self.send_request("GET", url, params=params)
        return resp
