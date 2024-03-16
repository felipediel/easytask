"""Models."""
from easytask.core.database import db
from easytask.core.models import BaseModel


class User(BaseModel):
    """User model."""

    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password_hash = db.Column(db.VARCHAR(130), nullable=False)


class TokenBlocklist(BaseModel):
    """Token blocklist model."""

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
