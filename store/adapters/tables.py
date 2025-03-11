from sqlalchemy import (
    Table,
    Column,
    Identity,
    ForeignKey,
    Uuid,
    Text,
    String,
    Boolean,
    Numeric,
    SmallInteger,
)
from sqlalchemy.orm import relationship

from adapters.db import mapper_registry
from domain.entities.user import User
from domain.entities.item import Item
from domain.value_objects.category import Category

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("user_id", Uuid, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("patronymic", String, nullable=True),
    Column("email", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
)

category_table = Table(
    "category",
    mapper_registry.metadata,
    Column("category_id", SmallInteger, Identity(always=True), primary_key=True),
    Column("name_ru", String, nullable=False),
    Column("name_en", String, nullable=False),
)

item_table = Table(
    "item",
    mapper_registry.metadata,
    Column("item_id", Uuid, primary_key=True),
    Column("name", String, nullable=False),
    Column("info", Text, nullable=False),
    Column("price", Numeric(10, 2), nullable=False),
    Column(
        "category_id", SmallInteger, ForeignKey("category.category_id"), nullable=False
    ),
)

mapper_registry.map_imperatively(User, user_table)
mapper_registry.map_imperatively(
    Category,
    category_table,
)
mapper_registry.map_imperatively(
    Item,
    item_table,
    properties={"category": relationship(Category, lazy="joined")},
)
