from litestar import MediaType, Request, Response
from litestar.exceptions import ValidationException


def validation_exception_handler(_: Request, exc: ValidationException) -> Response:
    error_content = ""
    if isinstance(exc.extra, list):
        error_content = str(
            {"errors": {err_msg["key"]: err_msg["message"] for err_msg in exc.extra}}
        )
    return Response(media_type=MediaType.TEXT, content=error_content, status_code=422)
