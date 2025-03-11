from litestar import Controller, post
from litestar.di import Provide

from domain import commands
from services import auth as auth_service
from adapters.unitofwork import IUnitOfWork, SQLAlchemyUnitOfWork


class AuthController(Controller):
    path = ""
    dependencies = {"uow": Provide(SQLAlchemyUnitOfWork, sync_to_thread=False)}

    @post("/login", exclude_from_auth=True)
    async def auth_user(self, data: commands.AuthUser, uow: IUnitOfWork) -> str:
        auth_token = await auth_service.auth_user(data, uow)
        return auth_token
