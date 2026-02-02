from collections.abc import AsyncIterator

from pytest import fixture, MonkeyPatch
from litestar import Litestar
from litestar.testing import AsyncTestClient

from app.main import app
from app.db.models import User


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client


@fixture(scope="function")
async def authed_test_client(monkeypatch: MonkeyPatch) -> AsyncIterator[AsyncTestClient[Litestar]]:
    mock_user = User(username="mockuser")

    monkeypatch.setattr("app.routes.article_controller.retrieve_user_handler", lambda *args, **kwargs: mock_user)

    async with AsyncTestClient(app=app) as client:
        yield client

