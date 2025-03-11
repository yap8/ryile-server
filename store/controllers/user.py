from typing import Any
from uuid import UUID

from litestar import Controller, Request, get, post, patch, delete
from litestar.di import Provide
from litestar.dto import DTOData

from domain import commands
from domain.entities.user import User
from controllers import dto
from controllers import guards
from services import user as user_service
from adapters.unitofwork import IUnitOfWork, SQLAlchemyUnitOfWork


class UserController(Controller):
    path = "/users"
    dependencies = {"uow": Provide(SQLAlchemyUnitOfWork, sync_to_thread=False)}

    @get("/{user_id:uuid}", return_dto=dto.ReturnUserDTO)
    async def get_user(self, user_id: UUID, uow: IUnitOfWork) -> User:
        user = await user_service.get_user(user_id, uow)
        return user

    @get("/me", return_dto=dto.ReturnUserDTO)
    async def get_current_user_info(self, request: "Request[User, Any, Any]") -> User:
        return request.user

    @post(return_dto=dto.ReturnUserDTO, exclude_from_auth=True)
    async def create_user(self, data: commands.CreateUser, uow: IUnitOfWork) -> User:
        user = await user_service.create_user(data, uow)
        return user

    @patch(
        "/{user_id:uuid}",
        dto=dto.UpdateUserDTO,
        guards=[guards.self_guard],
        return_dto=dto.ReturnUserDTO,
    )
    async def update_user(
        self,
        user_id: UUID,
        data: DTOData[commands.UpdateUser],
        uow: IUnitOfWork,
    ) -> User:
        command_data = data.create_instance(user_id=user_id)

        user = await user_service.update_user(command_data, uow)
        return user

    @delete(
        "/{user_id:uuid}",
        guards=[guards.self_or_admin_guard],
    )
    async def delete_user(self, user_id: UUID, uow: IUnitOfWork) -> None:
        await user_service.delete_user(user_id, uow)
