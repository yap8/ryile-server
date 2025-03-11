from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import registry
from sqlalchemy import MetaData

from config import settings


async_engine = create_async_engine(
    settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)

mapper_registry = registry(
    metadata=MetaData(naming_convention=settings.db.naming_convention)
)
