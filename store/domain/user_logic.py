from uuid import UUID, uuid4

from passlib.context import CryptContext
from email_validator import validate_email, EmailNotValidError

from domain import exceptions as domain_exc

from config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_if_email_is_valid(email: str):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise domain_exc.ValidationError(str(e))


def generate_user_id() -> UUID:
    return uuid4()


def get_password_hash(password: str):
    return password_context.hash(password + settings.security.salt)
