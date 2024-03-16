"""Views."""
from http import HTTPStatus

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
    create_refresh_token,
)
from flask_pydantic import validate

from flask import Blueprint

from easytask.core.cryptography import bcrypt
from easytask.core.exceptions import UnauthorizedError
from easytask.core.response import success_response
from easytask.core.schemas import SuccessResponseSchema

from .models import TokenBlocklist, User
from .schemas import (
    UserLoginSchema,
    UserLoginResponseSchema,
    UserRegisterSchema,
    RefreshTokenResponseSchema,
    UserSchema,
)

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["POST"])
@validate()
def register_user(
    body: UserRegisterSchema
) -> tuple[UserSchema, HTTPStatus]:
    """Register user."""
    new_user = User(**body.model_dump())
    new_user.password_hash = bcrypt.generate_password_hash(
        body.password.get_secret_value()
    )
    new_user.save()
    resp_data = UserSchema.model_validate(
        new_user, from_attributes=True
    )
    return success_response(resp_data, HTTPStatus.CREATED)


@auth_blueprint.route("/login", methods=["POST"])
@validate()
def login_user(
    body: UserLoginSchema
) -> tuple[UserLoginResponseSchema, HTTPStatus]:
    """Login user."""
    user = User.query.filter_by(email=body.email).first()
    if not user or not bcrypt.check_password_hash(
        user.password_hash, body.password.get_secret_value()
    ):
        raise UnauthorizedError(message="Invalid username or password")

    access_token = create_access_token(identity=user.email, fresh=True)
    refresh_token = create_refresh_token(identity=user.email)
    resp_data = UserLoginResponseSchema(
        access_token=access_token, refresh_token=refresh_token
    )
    return success_response(resp_data)


@auth_blueprint.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
@validate()
def logout_user() -> tuple[SuccessResponseSchema, HTTPStatus]:
    """Logout user."""
    token = get_jwt()
    jti = token["jti"]
    token_type = token["type"]
    blocklist = TokenBlocklist(jti=jti, type=token_type)
    blocklist.save()

    resp_data = SuccessResponseSchema(
        message=f"{token_type.capitalize()} revoked."
    )
    return success_response(resp_data)


@auth_blueprint.route("/refresh", methods=["POST"])
@validate()
@jwt_required(refresh=True)
def refresh_access_token() -> tuple[RefreshTokenResponseSchema, HTTPStatus]:
    """Refresh token."""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    resp_data = RefreshTokenResponseSchema(
        access_token=access_token
    )
    return success_response(resp_data)
