from litestar import Controller, get
from litestar.datastructures import State
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.tag_queries import TagQueries
from app.schemas.response_schemas import TagListResponse

sessionmaker = async_sessionmaker(expire_on_commit=False)


class TagController(Controller):
    path = "/api/tags"

    @get(exclude_from_auth=True)
    async def get_tags(self, state: State) -> TagListResponse:
        async with sessionmaker(bind=state.engine) as session:
            tags = await TagQueries.get_tags(session)
            tags = [tag.tag for tag in tags]
            return TagListResponse(tags=tags)
