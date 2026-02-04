from litestar import MediaType, Request, Response
from litestar.exceptions import ValidationException


def validation_exception_handler(_: Request, exc: ValidationException) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=exc.detail,
        status_code=422,
    )
