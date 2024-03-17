"""Token."""
from http import HTTPStatus
from flask_jwt_extended import JWTManager

from easytask.core.database import db
from easytask.core.response import error_response

from .models import TokenBlocklist

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload: dict) -> bool:
    """Check if JWT exists in the database blocklist."""
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@jwt.expired_token_loader
def expired_token_callback(*_):
    """Customize expired token response."""
    return error_response("Token has expired", HTTPStatus.UNAUTHORIZED)


@jwt.invalid_token_loader
def invalid_token_callback(_):
    """Customize invalid token response."""
    return error_response("Invalid token", HTTPStatus.UNAUTHORIZED)


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(*_):
    """Customize needs a fresh token response."""
    return error_response("A fresh token is required", HTTPStatus.UNAUTHORIZED)


@jwt.revoked_token_loader
def revoked_token_callback(*_):
    """Customize revoked token response."""
    return error_response("Token has been revoked", HTTPStatus.UNAUTHORIZED)


@jwt.token_verification_failed_loader
def token_verification_failed_callback(*_):
    """Customize token verification failed response."""
    return error_response("Token verification failed", HTTPStatus.UNAUTHORIZED)


@jwt.unauthorized_loader
def unauthorized_callback(_):
    """Customize unauthorized response."""
    return error_response("Unauthorized", HTTPStatus.UNAUTHORIZED)


@jwt.user_lookup_error_loader
def user_lookup_error_callback(*_):
    """Customize user lookup error response."""
    return error_response("User not found", HTTPStatus.NOT_FOUND)
