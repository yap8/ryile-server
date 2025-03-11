from dataclasses import asdict
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from domain import checks
from domain import commands
from domain.exceptions import AuthenticationError
from domain import user_logic, token_logic
from domain.entities.user import User
from adapters.unitofwork import IUnitOfWork

from utils.dataclasses import asdict_exclude_none


async def get_current_user(token: str, uow: IUnitOfWork) -> User:
    async with uow:
        payload = token_logic.decode_payload_from_token(token)

        try:
            user = await uow.user.get_by_id(payload["sub"])
        except NoResultFound:
            # по факту, если токен декодирован, а пользователя не нашлось,
            # то токен может быть скомпрометирован,
            # и тут надо это, как минимум, прологировать,
            # но для данного проекта это не является проблемой
            raise AuthenticationError("Пользователь не найден")
    return user


async def get_user(user_id: UUID, uow: IUnitOfWork) -> User:
    async with uow:
        user = await uow.user.get_by_id(user_id)
    return user


async def create_user(command: commands.CreateUser, uow: IUnitOfWork) -> User:
    async with uow:
        user_logic.check_if_email_is_valid(command.email)

        user_id = user_logic.generate_user_id()
        hashed_password = user_logic.get_password_hash(command.password)

        user = User(
            user_id=user_id,
            first_name=command.first_name,
            last_name=command.last_name,
            patronymic=command.patronymic,
            email=command.email,
            hashed_password=hashed_password,
        )

        await uow.user.create_one(asdict(user))
    return user


async def update_user(command: commands.UpdateUser, uow: IUnitOfWork) -> User:
    async with uow:
        if command.email:
            user_logic.check_if_email_is_valid(command.email)

        data_dict = asdict_exclude_none(command)
        data_dict.pop("user_id")
        checks.check_if_dict_is_not_empty(data_dict)

        if command.password:
            hashed_password = user_logic.get_password_hash(command.password)
            data_dict.pop("password")
            data_dict["hashed_password"] = hashed_password

        new_user = await uow.user.update_one(command.user_id, data_dict)
    return new_user


async def delete_user(user_id: UUID, uow: IUnitOfWork):
    async with uow:
        await uow.user.delete_one(user_id)
