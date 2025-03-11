from uuid import UUID
from typing import Annotated
from pathlib import Path
from litestar import Controller, get, post, patch, delete, status_codes
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.params import Body
from litestar.enums import RequestEncodingType
from litestar.datastructures import UploadFile
from litestar.exceptions import HTTPException
from litestar.response import File

from domain import commands
from domain.entities.item import Item
from domain.value_objects.category import Category
from services import item as item_service
from adapters.unitofwork import IUnitOfWork, SQLAlchemyUnitOfWork
from controllers import dto
from controllers import guards

from config import settings


def is_file_image(filename: str) -> bool:
    suffix = Path(filename).suffix.lower()
    image_suffixes = {".gif", ".jpg", ".jpeg", ".png"}
    return suffix in image_suffixes


class ItemController(Controller):
    path = "/items"
    dependencies = {"uow": Provide(SQLAlchemyUnitOfWork, sync_to_thread=False)}

    @post(guards=[guards.admin_guard], status_code=status_codes.HTTP_201_CREATED)
    async def create_item(self, data: commands.CreateItem, uow: IUnitOfWork) -> Item:
        item = await item_service.create_item(data, uow)
        return item

    @post(
        "/{item_id:uuid}/images",
        guards=[guards.admin_guard],
        status_code=status_codes.HTTP_201_CREATED,
    )
    async def add_item_image(
        self,
        item_id: UUID,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
    ) -> None:
        if not is_file_image(data.filename):
            raise HTTPException(detail="Файл не является изображением", status_code=400)

        file_path = Path(settings.image.path, str(item_id)).with_suffix(
            Path(data.filename).suffix
        )
        content = await data.read()
        with open(file_path, "wb") as file:
            file.write(content)

    @patch("/{item_id:uuid}", dto=dto.UpdateItemDTO, guards=[guards.admin_guard])
    async def update_item(
        self, item_id: UUID, data: DTOData[commands.UpdateItem], uow: IUnitOfWork
    ) -> Item:
        command_data = data.create_instance(item_id=item_id)

        updated_item = await item_service.update_item(command_data, uow)
        return updated_item

    @delete(
        "/{item_id:uuid}",
        guards=[guards.admin_guard],
        status_code=status_codes.HTTP_204_NO_CONTENT,
    )
    async def delete_item(self, item_id: UUID, uow: IUnitOfWork) -> None:
        await item_service.delete_item(item_id, uow)

    @get()
    async def get_all_items(self, uow: IUnitOfWork) -> list[Item]:
        items = await item_service.get_all_items(uow)
        return items

    @get("/{item_id:uuid}")
    async def get_item(self, item_id: UUID, uow: IUnitOfWork) -> Item:
        item = await item_service.get_item(item_id, uow)
        return item

    @get("/{item_id:uuid}/images", exclude_from_auth=True)
    async def get_item_image(self, item_id: UUID) -> File:
        try:
            image = next(file for file in settings.image.path.glob(f"{item_id}.*"))
            return File(image, filename=image.name)
        except StopIteration:
            raise HTTPException(
                detail="Изображение не найдено",
                status_code=status_codes.HTTP_404_NOT_FOUND,
            )

    @get("/categories")
    async def get_all_categories(self, uow: IUnitOfWork) -> list[Category]:
        categories = await item_service.get_all_categories(uow)
        return categories

    @get("/categories/{category_id:int}")
    async def get_category_items(
        self, category_id: int, uow: IUnitOfWork
    ) -> list[Item]:
        items = await item_service.get_items_by_category(category_id, uow)
        return items
