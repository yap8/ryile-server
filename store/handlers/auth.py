from typing import Any

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token

from domain.entities.user import User
from services.user import get_current_user
from adapters.unitofwork import SQLAlchemyUnitOfWork

from config import settings


ALGORITHM = settings.token.algorithm
SECRET_KEY = settings.token.key


async def retrieve_user_handler(
    token: Token, connection: "ASGIConnection[Any, Any, Any, Any]"
) -> User:
    uow = SQLAlchemyUnitOfWork()
    user = await get_current_user(token.encode(SECRET_KEY, ALGORITHM), uow)
    return user


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=SECRET_KEY,
    algorithm=ALGORITHM,
    exclude=["/schema"],
)
