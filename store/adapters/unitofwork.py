from logging import getLogger
from abc import ABC, abstractmethod

from adapters.db import async_session_factory
from adapters.repositories.user import (
    AbstractUserRepository,
    SQLAlchemyUserRepository,
)
from adapters.repositories.item import (
    AbstractItemRepository,
    SQLAlchemyItemRepository,
)


logger = getLogger(__name__)


class IUnitOfWork(ABC):
    user: AbstractUserRepository
    item: AbstractItemRepository

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            await self.rollback()
            logger.debug(
                "Rolled back transaction due to exception: %r with value %r.",
                exc_type,
                exc_value,
            )
        else:
            await self.commit()


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = SQLAlchemyUserRepository(self.session)
        self.item = SQLAlchemyItemRepository(self.session)

        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await super().__aexit__(exc_type, exc_value, exc_traceback)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
