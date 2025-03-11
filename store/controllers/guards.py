from litestar.connection import ASGIConnection
from litestar.handlers.base import BaseRouteHandler
from litestar.exceptions import PermissionDeniedException


def admin_guard(connection: ASGIConnection, handler: BaseRouteHandler) -> None:
    if not connection.user.is_admin:
        raise PermissionDeniedException(detail="Недостаточно прав")


def self_guard(connection: ASGIConnection, handler: BaseRouteHandler) -> None:
    user = connection.user
    user_id = connection.path_params["user_id"]

    if user.user_id != user_id:
        raise PermissionDeniedException(detail="Недостаточно прав")


def self_or_admin_guard(connection: ASGIConnection, handler: BaseRouteHandler) -> None:
    user = connection.user
    user_id = connection.path_params["user_id"]

    if not (user.user_id == user_id or user.is_admin):
        raise PermissionDeniedException(detail="Недостаточно прав")
