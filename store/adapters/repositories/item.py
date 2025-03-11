from uuid import UUID
from typing import Protocol, Sequence

from sqlalchemy import select, insert, update, delete

from domain.entities.item import Item
from domain.value_objects.category import Category
from adapters.repository import SQLAlchemyBaseRepository

from adapters.tables import item_table, category_table


class AbstractItemRepository(Protocol):
    async def create_one(self, item_data: dict): ...

    async def update_one(self, item_id: UUID, data: dict): ...

    async def delete_one(self, item_id: UUID): ...

    async def get_item_by_id(self, item_id: UUID) -> Item: ...

    async def get_items_by_category_id(self, category_id: int) -> Sequence[Item]: ...

    async def get_all_items(self) -> Sequence[Item]: ...

    async def get_all_categories(self) -> Sequence[Category]: ...


class SQLAlchemyItemRepository(SQLAlchemyBaseRepository):
    async def create_one(self, item_data: dict):
        stmt = insert(Item).values(**item_data)
        await self.session.execute(stmt)

    async def update_one(self, item_id: UUID, data: dict):
        stmt = update(Item).values(**data).filter(item_table.c.item_id == item_id)
        await self.session.execute(stmt)

    async def delete_one(self, item_id: UUID):
        stmt = delete(Item).filter(item_table.c.item_id == item_id)
        await self.session.execute(stmt)

    async def get_item_by_id(self, item_id: UUID) -> Item:
        stmt = select(Item).filter(item_table.c.item_id == item_id)
        res = await self.session.execute(stmt)
        result = res.scalar_one()
        return result

    async def get_items_by_category_id(self, category_id: int) -> Sequence[Item]:
        stmt = (
            select(Item)
            .join(
                category_table, item_table.c.category_id == category_table.c.category_id
            )
            .filter(item_table.c.category_id == category_id)
        )
        res = await self.session.execute(stmt)
        result = res.scalars().all()
        return result

    async def get_all_items(self) -> Sequence[Item]:
        stmt = select(Item)
        res = await self.session.execute(stmt)
        result = res.scalars().all()
        return result

    async def get_all_categories(self) -> Sequence[Category]:
        stmt = select(Category)
        res = await self.session.execute(stmt)
        result = res.scalars().all()
        return result
