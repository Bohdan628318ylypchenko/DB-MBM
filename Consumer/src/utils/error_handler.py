from typing import NoReturn
from src.errors import (
    http_exceptions,
    exceptions
)
from sqlalchemy.exc import NoResultFound


def raise_exception(exception: Exception) -> NoReturn:
    api_errors = {
        NoResultFound: http_exceptions.NOT_FOUND,
    }
    raise api_errors.get(type(exception), http_exceptions.INTERNAL_ERROR) # type: ignore
