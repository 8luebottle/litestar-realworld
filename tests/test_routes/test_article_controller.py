from litestar import Litestar
from litestar.status_codes import HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY
from litestar.testing import AsyncTestClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.auth.jwt_auth import jwt_auth
from app.db.models import User
from app.main import app


async def test_get_article_feed_no_token(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get("/api/articles/feed")

    assert response.status_code == HTTP_401_UNAUTHORIZED


async def test_get_article_feed_invalid_request(
    test_client: AsyncTestClient[Litestar],
) -> None:
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

    token = jwt_auth.create_token(identifier=str(user.id))

    response = await test_client.get(
        "/api/articles/feed/?limit=-1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
