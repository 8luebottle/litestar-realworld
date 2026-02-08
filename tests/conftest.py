from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture
from sqlalchemy.ext.asyncio import async_sessionmaker

from Conduit.auth.jwt_auth import jwt_auth
from Conduit.db.models import Base, User
from Conduit.main import app


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client


@fixture(scope="function")
async def token() -> str:
    sessionmaker = async_sessionmaker(expire_on_commit=False, bind=app.state.engine)
    async with sessionmaker() as session:
        user = User(
            username="mock_user",
            email="mock@mock.com",
            password="mock_pw",
            bio="mock_bio",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return jwt_auth.create_token(identifier=str(user.id))


@fixture(scope="function", autouse=True)
async def clean_db() -> AsyncGenerator[Any, Any]:
    yield
    engine = app.state.engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
