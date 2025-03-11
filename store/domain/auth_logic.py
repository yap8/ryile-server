from domain.user_logic import password_context
from domain import exceptions as domain_exc

from config import settings


def verify_password(password: str, hashed_password: str):
    password_verified = password_context.verify(
        password + settings.security.salt, hashed_password
    )
    if not password_verified:
        raise domain_exc.AuthenticationError("Пароль неверный")
