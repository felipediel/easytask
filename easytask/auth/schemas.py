"""Schemas."""
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)

from .models import User


class UserSchema(BaseModel):
    """User schema."""

    id: int | None = Field(title="Id")
    name: str = Field(title="Name")
    email: EmailStr = Field(title="E-mail")
    model_config = ConfigDict(extra="ignore")


class UserRegisterSchema(BaseModel):
    """User register schema."""

    name: str = Field(title="Name")
    email: EmailStr = Field(title="E-mail")
    password: SecretStr = Field(title="Password", exclude=True)
    model_config = ConfigDict(extra="ignore")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr) -> EmailStr:
        """Validate e-mail."""
        if User.query.filter_by(email=value).scalar():
            raise ValueError("E-mail already exists")
        return value


class UserLoginSchema(BaseModel):
    """User login schema."""

    email: EmailStr = Field(title="E-mail")
    password: SecretStr = Field(title="Password", exclude=True)


class UserLoginResponseSchema(BaseModel):
    """User login response schema."""

    access_token: str = Field(title="Access token")
    refresh_token: str = Field(title="Refresh token")


class RefreshTokenResponseSchema(BaseModel):
    """Refresh token response schema."""

    access_token: str = Field(title="Access token")
