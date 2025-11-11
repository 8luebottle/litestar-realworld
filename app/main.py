from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from sqlalchemy.ext.asyncio import create_async_engine

from .auth.jwt_auth import jwt_auth, require_authentication
from .db.models import Base
from .routes.article_controller import ArticleController
from .routes.profile_controller import ProfileController
from .routes.tag_controller import TagController
from .routes.user_controller import UserController


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


openapi_config = OpenAPIConfig(
    title="Litestar-RealWorld",
    version="0.0.0",
)

app = Litestar(
    [ArticleController, ProfileController, TagController, UserController],
    lifespan=[db_connection],
    on_app_init=[jwt_auth.on_app_init],
    guards=[require_authentication],
    openapi_config=openapi_config,
    debug=True,
)
