from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.connection import ASGIConnection
from litestar.exceptions import NotFoundException, PermissionDeniedException
from litestar.security.jwt import JWTAuth, Token
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .db.models import Base, User
from .db.queries import UserQueries
from .routes.article_controller import ArticleController
from .routes.profile_controller import ProfileController
from .routes.tag_controller import TagController
from .routes.user_controller import UserController

SECRET = "dummy-secret"


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(
            "postgresql+psycopg://testuser:testpass@localhost:5433/testdb", echo=True
        )
        app.state.engine = engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        await engine.dispose()


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User:
    state = connection.app.state
    sessionmaker = async_sessionmaker(expire_on_commit=False)
    async with sessionmaker(bind=state.engine) as session:
        try:
            user = await UserQueries.get_by_id(token.sub, session)
            return user
        except NotFoundException:
            raise PermissionDeniedException()


jwt_auth = JWTAuth[User](
    token_secret=SECRET,
    retrieve_user_handler=retrieve_user_handler,
)


app = Litestar(
    [ArticleController, ProfileController, TagController, UserController],
    lifespan=[db_connection],
    security=[jwt_auth],
    debug=True,
)
