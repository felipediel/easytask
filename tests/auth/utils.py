"""Utils."""
from easytask.auth.models import User
from easytask.core.cryptography import bcrypt


def create_test_user(
    name: str = "John Doe",
    email: str = "john@doe.com",
    password: str = "johnnybegoodtonight",
):
    """Create a test user and add it to the database."""
    new_user = User(
        name=name,
        email=email,
        password_hash=bcrypt.generate_password_hash(password),
    )
    new_user.save()
    return new_user
