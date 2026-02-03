from collections.abc import AsyncIterator

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from app.main import app

# @fixture(scope="function")
# async def mock_user() -> User:
#     sessionmaker = async_sessionmaker(expire_on_commit=False)
#     async with sessionmaker(bind=app.state.engine) as session:
#         user = User(
#             username="mock_user",
#             email="mock_email@mock.com",
#             password="mock_pw",
#             bio="mock_bio",
#             image=None
#         )
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#     return user


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client
