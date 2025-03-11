from uuid import UUID, uuid4
from decimal import Decimal

from domain import exceptions as exc


def check_price(price: Decimal):
    if price < 0:
        raise exc.ValidationError("Цена товара не может быть отрицательной")


def generate_item_id() -> UUID:
    return uuid4()
