from uuid import UUID
from typing import Protocol

from sqlalchemy import select, insert, update, delete

from domain.entities.user import User
from adapters.repository import SQLAlchemyBaseRepository

from adapters.tables import user_table


class AbstractUserRepository(Protocol):
    async def get_by_id(self, user_id: UUID) -> User: ...

    async def get_by_email(self, email: str) -> User: ...

    async def create_one(self, user: dict): ...

    async def update_one(self, user_id: UUID, data: dict) -> User: ...

    async def delete_one(self, user_id: UUID): ...


class SQLAlchemyUserRepository(SQLAlchemyBaseRepository):
    async def get_by_id(self, user_id: UUID) -> User:
        stmt = select(User).filter(user_table.c.user_id == user_id)
        res = await self.session.execute(stmt)
        result = res.scalar_one()
        return result

    async def get_by_email(self, email: str) -> User:
        stmt = select(User).filter(user_table.c.email == email)
        res = await self.session.execute(stmt)
        result = res.scalar_one()
        return result

    async def create_one(self, user: dict):
        stmt = insert(User).values(**user)
        await self.session.execute(stmt)

    async def update_one(self, user_id: UUID, data: dict) -> User:
        stmt = (
            update(User)
            .values(**data)
            .filter(user_table.c.user_id == user_id)
            .returning(User)
        )
        res = await self.session.execute(stmt)
        result = res.scalar_one()
        return result

    async def delete_one(self, user_id: UUID):
        stmt = delete(User).filter(user_table.c.user_id == user_id)
        await self.session.execute(stmt)
