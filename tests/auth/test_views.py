"""Test views."""
from http import HTTPStatus

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, url_for
from flask.testing import FlaskClient

from easytask.auth.models import User, TokenBlocklist

from tests.common.utils import assert_response_error

from .utils import create_test_user


def test_register_user(app: Flask, client: FlaskClient, database: SQLAlchemy):
    """Test that it is possible to register a user."""
    test_user_data = {
        "name": "John Doe",
        "email": "john@doe.com",
        "password": "johnnybegoodtonight"
    }

    with app.test_request_context():
        response = client.post(
            url_for("auth.register_user"), json=test_user_data
        )

    assert response.status_code == HTTPStatus.CREATED, response.json
    response_data = response.json
    assert "id" in response_data
    assert response_data["name"] == test_user_data["name"]
    assert response_data["email"] == test_user_data["email"]

    # Check if the user exists in the database
    user = User.query.filter_by(email=test_user_data["email"]).first()

    assert user is not None
    assert user.name == test_user_data["name"]
    assert user.email == test_user_data["email"]


def test_register_same_user_twice_returns_400(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that an attempt to register the same user returns 400."""
    test_user_data = {
        "name": "John Doe",
        "email": "john@doe.com",
        "password": "johnnybegoodtonight"
    }
    create_test_user(**test_user_data)

    # These fields can change
    test_user_data["name"] = "John Donuts"
    test_user_data["password"] = "johnnybegoodtomorrow"

    with app.test_request_context():
        response = client.post(
            url_for("auth.register_user"), json=test_user_data
        )

    assert_response_error(response, "Validation error", HTTPStatus.BAD_REQUEST)

    response_data = response.json
    error = response_data["error"]
    assert "context" in error
    context = error["context"]
    assert "body_params" in context
    body_params = context["body_params"]
    assert len(body_params) == 1
    error_detail = body_params[0]
    assert isinstance(error_detail, dict)
    assert error_detail.get("type") == "value_error"
    assert error_detail.get("loc") == ["email"]
    assert error_detail.get("msg") == "Value error, E-mail already exists"
    assert error_detail.get("input") == "john@doe.com"


def test_login_user(app: Flask, client: FlaskClient, database: SQLAlchemy):
    """Test user login."""
    test_user_data = {
        "email": "john@doe.com",
        "password": "johnnybegoodtonight"
    }
    create_test_user(**test_user_data)

    with app.test_request_context():
        response = client.post(
            url_for("auth.login_user"), json=test_user_data
        )

    assert response.status_code == HTTPStatus.OK, response.json
    resp_data = response.json
    assert "access_token" in resp_data
    assert "refresh_token" in resp_data


def test_login_wrong_username_returns_401(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that login attempt with wrong username returns 401."""
    test_user_data = {
        "email": "john@doe.com",
        "password": "johnnybegoodtonight"
    }
    create_test_user(**test_user_data)

    test_user_data["password"] = "johnnybegoodtomorrow"

    with app.test_request_context():
        response = client.post(
            url_for("auth.login_user"), json=test_user_data
        )

    assert_response_error(
        response, "Invalid username or password", HTTPStatus.UNAUTHORIZED
    )


def test_login_wrong_password_returns_401(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that login attempt with wrong password returns 401."""
    test_user_data = {
        "email": "john@doe.com",
        "password": "johnnybegoodtonight"
    }
    create_test_user(**test_user_data)

    test_user_data["password"] = "johnnybegoodtomorrow"

    with app.test_request_context():
        response = client.post(
            url_for("auth.login_user"), json=test_user_data
        )

    assert_response_error(
        response, "Invalid username or password", HTTPStatus.UNAUTHORIZED
    )


def test_logout_user_revoke_access_token(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test user logout (revoke access token)."""
    test_user = create_test_user()
    access_token = create_access_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    with app.test_request_context():
        response = client.delete(url_for("auth.logout_user"), headers=headers)

    assert response.status_code == HTTPStatus.OK, response.json
    response_data = response.json
    assert "message" in response_data
    assert response_data["message"] == "Access revoked."

    jti = decode_token(access_token, allow_expired=True)["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()

    assert token is not None
    assert token.type == "access"


def test_logout_user_revoke_refresh_token(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test user logout (revoke refresh token)."""
    test_user = create_test_user()
    refresh_token = create_refresh_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {refresh_token}"}

    with app.test_request_context():
        response = client.delete(url_for("auth.logout_user"), headers=headers)

    assert response.status_code == HTTPStatus.OK, response.json
    response_data = response.json
    assert "message" in response_data
    assert response_data["message"] == "Refresh revoked."

    jti = decode_token(refresh_token, allow_expired=True)["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()

    assert token is not None
    assert token.type == "refresh"


def test_refresh_access_token(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test refreshing access token."""
    test_user = create_test_user()
    refresh_token = create_refresh_token(identity=test_user.email)
    headers = {"Authorization": f"Bearer {refresh_token}"}

    with app.test_request_context():
        response = client.post(
            url_for("auth.refresh_access_token"), headers=headers
        )

    assert response.status_code == HTTPStatus.OK, response.json
    response_data = response.json
    assert "access_token" in response_data
    decoded_token = decode_token(response_data["access_token"])
    assert decoded_token["sub"] == test_user.email


def test_refresh_access_with_revoked_token_returns_401(
    app: Flask, client: FlaskClient, database: SQLAlchemy
):
    """Test that an attempt to refresh with a revoked token returns 401."""
    test_user = create_test_user()
    refresh_token = create_refresh_token(identity=test_user.email)

    jti = decode_token(refresh_token, allow_expired=True)["jti"]
    blocklist = TokenBlocklist(jti=jti, type="refresh")
    blocklist.save()

    headers = {"Authorization": f"Bearer {refresh_token}"}

    with app.test_request_context():
        response = client.post(
            url_for("auth.refresh_access_token"), headers=headers
        )

    assert_response_error(
        response, "Token has been revoked", HTTPStatus.UNAUTHORIZED
    )
