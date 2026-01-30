from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig
from sqlalchemy.ext.asyncio import create_async_engine

from .auth.jwt_auth import jwt_auth
from .db.models import Base
from .routes.article_controller import ArticleController
from .routes.profile_controller import ProfileController
from .routes.tag_controller import TagController
from .routes.user_controller import UserController
from .settings import settings


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(settings.DB_URL, echo=settings.DB_ECHO)
        app.state.engine = engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        await engine.dispose()


cors_config = CORSConfig(allow_origins=["*"])


openapi_config = OpenAPIConfig(
    title="Litestar-RealWorld",
    version="0.0.0",
)

app = Litestar(
    [ArticleController, ProfileController, TagController, UserController],
    lifespan=[db_connection],
    on_app_init=[jwt_auth.on_app_init],
    openapi_config=openapi_config,
    cors_config=cors_config,
    debug=settings.DEBUG,
)
