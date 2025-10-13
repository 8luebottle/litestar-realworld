from litestar import Controller, get

from app.schemas.response_schemas import TagListResponse


class TagController(Controller):
    path = "/api/tags"

    @get()
    async def get_tags(self) -> TagListResponse:
        pass
