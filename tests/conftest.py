from collections.abc import AsyncIterator

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from app.main import app


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client
