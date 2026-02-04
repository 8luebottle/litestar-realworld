from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from app.db.models import Base
from app.main import app


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client


@fixture(scope="function", autouse=True)
async def clean_db() -> AsyncGenerator[Any, Any]:
    yield
    engine = app.state.engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
