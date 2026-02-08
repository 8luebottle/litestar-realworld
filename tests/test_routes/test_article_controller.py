from typing import Any

import pytest
from litestar import Litestar
from litestar.status_codes import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from litestar.testing import AsyncTestClient


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
    query_str: str, expected: str, test_client: AsyncTestClient[Litestar], token: str
) -> None:
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


@pytest.mark.parametrize(
    "body,expected",
    [
        (
            {"article": {"title": "mock title", "description": "mock description"}},
            "{'errors': {'article': 'Object missing required field `body`'}}",
        ),
        (
            {"article": {"description": "mock description", "body": "mock body"}},
            "{'errors': {'article': 'Object missing required field `title`'}}",
        ),
        (
            {"article": {"title": "mock title", "body": "mock body"}},
            "{'errors': {'article': 'Object missing required field `description`'}}",
        ),
        ({}, "{'errors': {'data': 'Object missing required field `article`'}}"),
    ],
)
async def test_create_article_invalid_request(
    body: dict[str, Any],
    expected: str,
    test_client: AsyncTestClient[Litestar],
    token: str,
) -> None:
    response = await test_client.post(
        "/api/articles/", headers={"Authorization": f"Bearer {token}"}, json=body
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert str(response.content, "utf-8") == expected


async def test_update_article_no_token(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.put("/api/articles/non-existent")

    assert response.status_code == HTTP_401_UNAUTHORIZED


async def test_update_article_slug_not_found(
    test_client: AsyncTestClient[Litestar], token: str
) -> None:
    response = await test_client.put(
        "/api/articles/non-existent-article",
        headers={"Authorization": f"Bearer {token}"},
        json={"article": {}},
    )

    assert response.status_code == HTTP_404_NOT_FOUND


async def test_update_article_invalid_request(
    test_client: AsyncTestClient, article_slug: str, author_token: str
) -> None:
    response = await test_client.put(
        f"/api/articles/{article_slug}",
        headers={"Authorization": f"Bearer {author_token}"},
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert str(response.content, "utf-8") == "{'errors': {'data': \"'data'\"}}"


async def test_update_article_forbidden(
    test_client: AsyncTestClient, token: str, article_slug: str
) -> None:
    response = await test_client.put(
        f"/api/articles/{article_slug}",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )

    assert response.status_code == HTTP_403_FORBIDDEN
