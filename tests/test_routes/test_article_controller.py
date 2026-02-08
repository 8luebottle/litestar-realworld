import pytest
from litestar import Litestar
from litestar.status_codes import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from litestar.testing import AsyncTestClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from Conduit.auth.jwt_auth import jwt_auth
from Conduit.db.models import User
from Conduit.main import app


@pytest.mark.parametrize(
    "query_str,expected",
    [
        (
            "limit=-1&offset=-1",
            "{'errors': {'limit': 'Expected `int` >= 1', 'offset': 'Expected `int` >= 0'}}",
        ),
        ("limit=-1", "{'errors': {'limit': 'Expected `int` >= 1'}}"),
        ("offset=-1", "{'errors': {'offset': 'Expected `int` >= 0'}}"),
    ],
)
async def test_get_articles_invalid_request(
    query_str: str,
    expected: str,
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get(f"/api/articles/?{query_str}")

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert str(response.content, "utf-8") == expected


@pytest.mark.parametrize(
    "query_str,expected",
    [
        ("author=not here", '{"status_code":404,"detail":"Author id not found"}'),
        ("favorited=not here", '{"status_code":404,"detail":"Favorited id not found"}'),
    ],
)
async def test_get_articles_not_found(
    query_str: str,
    expected: str,
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get(f"/api/articles/?{query_str}")

    assert response.status_code == HTTP_404_NOT_FOUND
    assert str(response.content, "utf-8") == expected


async def test_get_article_feed_no_token(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get("/api/articles/feed")

    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "query_str,expected",
    [
        (
            "limit=-1&offset=-1",
            "{'errors': {'limit': 'Expected `int` >= 1', 'offset': 'Expected `int` >= 0'}}",
        ),
        ("limit=-1", "{'errors': {'limit': 'Expected `int` >= 1'}}"),
        ("offset=-1", "{'errors': {'offset': 'Expected `int` >= 0'}}"),
    ],
)
async def test_get_article_feed_invalid_request(
    query_str: str, expected: str, test_client: AsyncTestClient[Litestar]
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
        f"/api/articles/feed/?{query_str}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert str(response.content, "utf-8") == expected


async def test_get_article_not_found(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.get("/api/articles/non-existent-article")

    assert response.status_code == HTTP_404_NOT_FOUND


async def test_create_article_no_token(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.post("/api/articles/")

    assert response.status_code == HTTP_401_UNAUTHORIZED
