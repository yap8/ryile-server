from litestar import Request, Response, status_codes
from litestar.exceptions import HTTPException

from sqlalchemy.exc import NoResultFound, IntegrityError

from domain import exceptions as domain_exc


def sql_no_result_found_handler(request: Request, exc: NoResultFound) -> Response:
    return Response(
        content={
            "detail": str(exc),
        },
        status_code=status_codes.HTTP_404_NOT_FOUND,
    )


def integrity_handler(request: Request, exc: IntegrityError) -> Response:
    return Response(
        content={"detail": "Одно из полей неверно заполнено"},
        status_code=status_codes.HTTP_400_BAD_REQUEST,
    )


def auth_handler(request: Request, exc: domain_exc.AuthenticationError) -> Response:
    return Response(
        content={
            "detail": str(exc),
        },
        status_code=status_codes.HTTP_401_UNAUTHORIZED,
    )


def not_falid_handler(request: Request, exc: domain_exc.ValidationError) -> Response:
    return Response(
        content={
            "detail": str(exc),
        },
        status_code=status_codes.HTTP_400_BAD_REQUEST,
    )


def http_exc_handler(request: Request, exc: HTTPException) -> Response:
    return Response(content={"detail": exc.detail}, status_code=exc.status_code)


def base_exc_handler(request: Request, exc: Exception):
    raise exc


exception_handlers = {
    domain_exc.ValidationError: not_falid_handler,
    domain_exc.AuthenticationError: auth_handler,
    NoResultFound: sql_no_result_found_handler,
    IntegrityError: integrity_handler,
    HTTPException: http_exc_handler,
    Exception: base_exc_handler,
}
