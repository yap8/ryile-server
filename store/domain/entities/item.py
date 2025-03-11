from dataclasses import dataclass
from uuid import UUID

from domain.value_objects.category import Category


@dataclass
class Item:
    item_id: UUID
    name: str
    info: str
    price: str
    category: Category
