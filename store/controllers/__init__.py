from controllers.user import UserController
from controllers.auth import AuthController
from controllers.item import ItemController


controllers = [
    UserController,
    AuthController,
    ItemController,
]

__all__ = ["controllers"]
