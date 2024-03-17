"""Test views."""
from http import HTTPStatus
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

from requests.exceptions import RequestException, Timeout

from flask import Flask, url_for
from flask.testing import FlaskClient

from tests.auth.utils import create_test_user
from tests.common.utils import assert_response_error, open_sample

CLIENT_SESSION_CLS_PATH = "easytask.tasks.client.requests.Session"


def test_get_task_list(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that an user can retrieve a task list."""
    test_user = create_test_user()
    access_token = create_access_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = app.config["TASK_SERVICE_URL"]

    with (
        app.test_request_context(),
        patch(CLIENT_SESSION_CLS_PATH) as mock_session_cls,
        open_sample("task_list.json", "rb") as file
    ):
        mock_data = file.read()
        mock_session = mock_session_cls.return_value
        mock_session.send.return_value.url = api_url
        mock_session.send.return_value.status_code = 200
        mock_session.send.return_value.content = mock_data
        mock_session.send.return_value.headers = {
            "Content-Type": "application/json"
        }
        response = client.get(url_for("tasks.get_task_list"), headers=headers)

    assert response.status_code == HTTPStatus.OK
    resp_data = response.json
    assert isinstance(resp_data, list)
    assert len(resp_data) == 5

    assert resp_data[0] == {"id": 1, "title": "delectus aut autem"}
    assert resp_data[1] == {"id": 2, "title": "quis ut nam facilis et officia"}
    assert resp_data[2] == {"id": 3, "title": "fugiat veniam minus"}
    assert resp_data[3] == {"id": 4, "title": "et porro tempora"}
    assert resp_data[4] == {"id": 5, "title": "laboriosam mollitia et enim"}


def test_get_task_list_without_token_returns_401(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that a 401 status code is returned for an unauthorized request."""
    api_url = app.config["TASK_SERVICE_URL"]

    with (
        app.test_request_context(),
        patch(CLIENT_SESSION_CLS_PATH) as mock_session_cls,
        open_sample("task_list.json", "rb") as file
    ):
        mock_data = file.read()
        mock_session = mock_session_cls.return_value
        mock_session.send.return_value.url = api_url
        mock_session.send.return_value.status_code = 200
        mock_session.send.return_value.content = mock_data
        mock_session.send.return_value.headers = {
            "Content-Type": "application/json"
        }
        response = client.get(url_for("tasks.get_task_list"))

    assert_response_error(
        response, "Unauthorized", HTTPStatus.UNAUTHORIZED
    )


def test_get_task_list_with_invalid_token_returns_401(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that a 401 status code is returned for an unauthorized request."""
    api_url = app.config["TASK_SERVICE_URL"]
    headers = {"Authorization": "Bearer HighHopes"}

    with (
        app.test_request_context(),
        patch(CLIENT_SESSION_CLS_PATH) as mock_session_cls,
        open_sample("task_list.json", "rb") as file
    ):
        mock_data = file.read()
        mock_session = mock_session_cls.return_value
        mock_session.send.return_value.url = api_url
        mock_session.send.return_value.status_code = 200
        mock_session.send.return_value.content = mock_data
        mock_session.send.return_value.headers = {
            "Content-Type": "application/json"
        }
        response = client.get(url_for("tasks.get_task_list"), headers=headers)

    assert_response_error(
        response, "Invalid token", HTTPStatus.UNAUTHORIZED
    )


def test_get_task_list_invalid_service_resp_schema_returns_502(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that a 502 status code is returned for an invalid response schema.

    This test verifies that if an invalid response schema is received from the
    service when retrieving a task list, a 502 status code is returned.
    """
    test_user = create_test_user()
    access_token = create_access_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = app.config["TASK_SERVICE_URL"]

    with (
        app.test_request_context(),
        patch(CLIENT_SESSION_CLS_PATH) as mock_session_cls,
        open_sample("task_list_invalid_schema.json", "rb") as file
    ):
        mock_data = file.read()
        mock_session = mock_session_cls.return_value
        mock_session.send.return_value.url = api_url
        mock_session.send.return_value.status_code = 200
        mock_session.send.return_value.content = mock_data
        mock_session.send.return_value.headers = {
            "Content-Type": "application/json"
        }
        response = client.get(url_for("tasks.get_task_list"), headers=headers)

    assert_response_error(
        response,
        "Invalid responses from another server/proxy",
        HTTPStatus.BAD_GATEWAY,
    )


def test_get_task_list_allows_extra_keys(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that extra keys are allowed in the service response.

    This test verifies that extra keys received from the server when retrieving
    a task list are allowed and ignored.
    """
    test_user = create_test_user()
    access_token = create_access_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = app.config["TASK_SERVICE_URL"]

    with (
        app.test_request_context(),
        patch(CLIENT_SESSION_CLS_PATH) as mock_session_cls,
        open_sample("task_list_extra_keys.json", "rb") as file
    ):
        mock_data = file.read()
        mock_session = mock_session_cls.return_value
        mock_session.send.return_value.url = api_url
        mock_session.send.return_value.status_code = 200
        mock_session.send.return_value.content = mock_data
        mock_session.send.return_value.headers = {
            "Content-Type": "application/json"
        }
        response = client.get(url_for("tasks.get_task_list"), headers=headers)

    assert response.status_code == HTTPStatus.OK
    resp_data = response.json
    assert isinstance(resp_data, list)
    assert len(resp_data) == 5

    assert resp_data[0] == {"id": 1, "title": "delectus aut autem"}
    assert resp_data[1] == {"id": 2, "title": "quis ut nam facilis et officia"}
    assert resp_data[2] == {"id": 3, "title": "fugiat veniam minus"}
    assert resp_data[3] == {"id": 4, "title": "et porro tempora"}
    assert resp_data[4] == {"id": 5, "title": "laboriosam mollitia et enim"}


def test_get_task_list_timeout_returns_504(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that a timeout error in the request to the service returns 504."""
    test_user = create_test_user()
    access_token = create_access_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    with (
        app.test_request_context(),
        patch(CLIENT_SESSION_CLS_PATH) as mock_session_cls
    ):
        mock_session = mock_session_cls.return_value
        mock_session.send.side_effect = Timeout()
        response = client.get(url_for("tasks.get_task_list"), headers=headers)

    assert_response_error(
        response,
        "The gateway server did not receive a timely response",
        HTTPStatus.GATEWAY_TIMEOUT,
    )


def test_get_task_list_request_exception_returns_502(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that an exception in the request to the service returns 502."""    
    test_user = create_test_user()
    access_token = create_access_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    with (
        app.test_request_context(),
        patch(CLIENT_SESSION_CLS_PATH) as mock_session_cls
    ):
        mock_session = mock_session_cls.return_value
        mock_session.send.side_effect = RequestException()
        response = client.get(url_for("tasks.get_task_list"), headers=headers)

    assert_response_error(
        response,
        "Invalid responses from another server/proxy",
        HTTPStatus.BAD_GATEWAY,
    )
