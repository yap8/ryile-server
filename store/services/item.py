from dataclasses import asdict
from uuid import UUID

from domain import checks
from domain import commands
from domain import item_logic
from domain.entities.item import Item
from domain.value_objects.category import Category
from adapters.unitofwork import IUnitOfWork
from utils.dataclasses import asdict_exclude_none


async def create_item(command: commands.CreateItem, uow: IUnitOfWork) -> Item:
    async with uow:
        item_logic.check_price(command.price)

        item_data = asdict(command)
        item_id = item_logic.generate_item_id()
        item_data["item_id"] = item_id

        await uow.item.create_one(item_data)
        item = await uow.item.get_item_by_id(item_id)
    return item


async def update_item(command: commands.UpdateItem, uow: IUnitOfWork) -> Item:
    async with uow:
        if command.price:
            item_logic.check_price(command.price)

        data_dict = asdict_exclude_none(command)
        data_dict.pop("item_id")

        checks.check_if_dict_is_not_empty(data_dict)

        await uow.item.update_one(command.item_id, data_dict)
        item = await uow.item.get_item_by_id(command.item_id)
    return item


async def delete_item(item_id: UUID, uow: IUnitOfWork):
    async with uow:
        await uow.item.delete_one(item_id)


async def get_item(item_id: UUID, uow: IUnitOfWork) -> Item:
    async with uow:
        item = await uow.item.get_item_by_id(item_id)
    return item


async def get_items_by_category(category_id: int, uow: IUnitOfWork) -> list[Item]:
    async with uow:
        items = list(await uow.item.get_items_by_category_id(category_id))
    return items


async def get_all_items(uow: IUnitOfWork) -> list[Item]:
    async with uow:
        items = list(await uow.item.get_all_items())
    return items


async def get_all_categories(uow: IUnitOfWork) -> list[Category]:
    async with uow:
        categories = list(await uow.item.get_all_categories())
    return categories
