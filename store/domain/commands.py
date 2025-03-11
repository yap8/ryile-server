from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateUser(Command):
    first_name: str
    last_name: str
    patronymic: str
    email: str
    password: str


@dataclass()
class UpdateUser(Command):
    user_id: UUID
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    email: str | None = None
    password: str | None = None


@dataclass
class AuthUser(Command):
    email: str
    password: str


@dataclass
class CreateItem(Command):
    name: str
    info: str
    price: Decimal
    category_id: int


@dataclass
class UpdateItem(Command):
    item_id: UUID
    name: str | None = None
    info: str | None = None
    price: Decimal | None = None
    category_id: int | None = None
