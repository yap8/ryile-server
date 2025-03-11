from sqlalchemy.exc import NoResultFound

from domain import commands
from domain import auth_logic, token_logic
from adapters.unitofwork import IUnitOfWork

from domain.exceptions import AuthenticationError


async def auth_user(command: commands.AuthUser, uow: IUnitOfWork) -> str:
    async with uow:
        try:
            user = await uow.user.get_by_email(command.email)
        except NoResultFound:
            raise AuthenticationError("Пользователь не найден")

        auth_logic.verify_password(command.password, user.hashed_password)

        payload = {"sub": str(user.user_id)}
        token = token_logic.encode_payload_to_token(payload)
    return token
