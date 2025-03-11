from litestar.dto import DataclassDTO, DTOConfig

from domain import commands
from domain.entities.user import User


class UpdateUserDTO(DataclassDTO[commands.UpdateUser]):
    config = DTOConfig(exclude={"user_id"})


class ReturnUserDTO(DataclassDTO[User]):
    config = DTOConfig(exclude={"hashed_password"})


class UpdateItemDTO(DataclassDTO[commands.UpdateItem]):
    config = DTOConfig(exclude={"item_id"})
