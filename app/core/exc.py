from __future__ import annotations

from typing import Any, Callable, Dict, Final, Optional, Type, Union

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

from exc import ApplicationError
from logger import logger

STATUS_CODES: Final[Dict[Any, Callable[[Any], int]]] = {
    ApplicationError: lambda _: status.HTTP_500_INTERNAL_SERVER_ERROR,
    HTTPException: lambda value: value.status_code,
    RequestValidationError: lambda _: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ValidationError: lambda _: status.HTTP_422_UNPROCESSABLE_ENTITY,
}


def add_exception_handler(
    application: FastAPI,
    exception_class_or_status_code: Union[Type[BaseException], int],
    error: Optional[str] = None,
) -> None:
    def default_exception_handler(
        request: Request,  # noqa
        exception: Exception,
    ) -> None:
        if hasattr(default_exception_handler, "__error__"):
            error = default_exception_handler.__error__
        elif hasattr(exception, "detail"):
            error = exception.detail
        else:
            error = "UNKNOWN_ERROR"

        if hasattr(default_exception_handler, "__status_code__"):
            status_code = default_exception_handler.__status_code__
        else:
            status_code = STATUS_CODES.get(type(exception), status.HTTP_500_INTERNAL_SERVER_ERROR)(
                exception
            )

        logger.debug(
            "Error: status code(%s): %s: %s" % (status_code, type(exception), str(exception))
        )

        return JSONResponse(
            status_code=status_code,
            content={
                "ok": False,
                "error": error,
                "error_code": status_code,
            },
        )

    function = default_exception_handler
    if isinstance(exception_class_or_status_code, int):
        function.__status_code__ = exception_class_or_status_code
    if error:
        function.__error__ = error

    application.add_exception_handler(exception_class_or_status_code, function)


def add_default_error_handlers(application: FastAPI) -> None:
    DEFAULT_NAME: Final[str] = "HTTP_4"
    for status_code in filter(lambda x: x.startswith(DEFAULT_NAME), status.__all__):
        _http, _code, *name = status_code.split("_")
        add_exception_handler(
            application=application,
            exception_class_or_status_code=getattr(status, status_code),
            error="_".join(name),
        )


def create_exception_handlers(application: FastAPI) -> None:
    add_default_error_handlers(application=application)
    add_exception_handler(application=application, exception_class_or_status_code=ApplicationError)
    add_exception_handler(application=application, exception_class_or_status_code=HTTPException)
    add_exception_handler(
        application=application,
        exception_class_or_status_code=RequestValidationError,
        error="REQUEST_VALIDATION_FAILED",
    )
    add_exception_handler(
        application=application,
        exception_class_or_status_code=ValidationError,
        error="REQUEST_VALIDATION_FAILED",
    )
