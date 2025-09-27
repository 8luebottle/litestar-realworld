from litestar import Controller, get
from app.schemas import TagList


class TagController(Controller):
    path = "/api/tags"

    @get()
    def get_tags() -> TagList:
        pass
