"""Article controller happy path tests — OpenSpec articles 스펙 기반."""

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.testing import AsyncTestClient

from tests.conftest import create_user_in_db, get_token_for_user, unique_id

ARTICLES = "/api/articles"


async def test_create_article(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"author_{uid}", f"author_{uid}@test.com")
    token = await get_token_for_user(user)

    response = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Test Article {uid}",
                "description": "A test article",
                "body": "Article body content",
            }
        },
    )

    assert response.status_code == HTTP_201_CREATED
    data = response.json()["article"]
    assert data["title"] == f"Test Article {uid}"
    assert data["description"] == "A test article"
    assert data["body"] == "Article body content"
    assert data["favorited"] is False
    assert data["favoritesCount"] == 0
    assert data["author"]["username"] == f"author_{uid}"


async def test_create_article_with_tags(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"tagger_{uid}", f"tagger_{uid}@test.com")
    token = await get_token_for_user(user)

    response = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Tagged Article {uid}",
                "description": "Tagged",
                "body": "Body",
                "tagList": ["python", "litestar"],
            }
        },
    )

    assert response.status_code == HTTP_201_CREATED
    tags = response.json()["article"]["tagList"]
    assert "python" in tags
    assert "litestar" in tags


async def test_get_article_by_slug(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"getart_{uid}", f"getart_{uid}@test.com")
    token = await get_token_for_user(user)

    create_resp = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Get Article {uid}",
                "description": "Get test",
                "body": "Get body",
            }
        },
    )
    slug = create_resp.json()["article"]["slug"]

    response = await test_client.get(f"{ARTICLES}/{slug}")

    assert response.status_code == HTTP_200_OK
    data = response.json()["article"]
    assert data["slug"] == slug
    assert data["body"] == "Get body"


async def test_get_articles_list(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.get(ARTICLES)

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert "articles" in data
    assert "articlesCount" in data
    assert isinstance(data["articles"], list)


async def test_get_articles_with_limit_offset(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get(f"{ARTICLES}?limit=5&offset=0")

    assert response.status_code == HTTP_200_OK
    assert len(response.json()["articles"]) <= 5


async def test_get_articles_filter_by_author(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"fltauth_{uid}", f"fltauth_{uid}@test.com")
    token = await get_token_for_user(user)

    await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Filter Author {uid}",
                "description": "Filter",
                "body": "Body",
            }
        },
    )

    response = await test_client.get(f"{ARTICLES}?author=fltauth_{uid}")

    assert response.status_code == HTTP_200_OK
    articles = response.json()["articles"]
    assert len(articles) >= 1
    assert all(a["author"]["username"] == f"fltauth_{uid}" for a in articles)


async def test_get_article_feed(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    reader = await create_user_in_db(f"reader_{uid}", f"reader_{uid}@test.com")
    writer = await create_user_in_db(f"writer_{uid}", f"writer_{uid}@test.com")
    reader_token = await get_token_for_user(reader)
    writer_token = await get_token_for_user(writer)

    # Writer creates an article
    await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {writer_token}"},
        json={
            "article": {
                "title": f"Feed Article {uid}",
                "description": "Feed test",
                "body": "Feed body",
            }
        },
    )

    # Reader follows writer
    await test_client.post(
        f"/api/profiles/writer_{uid}/follow",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    response = await test_client.get(
        f"{ARTICLES}/feed",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert "articles" in data
    assert "articlesCount" in data


async def test_update_article(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"upd_{uid}", f"upd_{uid}@test.com")
    token = await get_token_for_user(user)

    create_resp = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Update Article {uid}",
                "description": "Before update",
                "body": "Before body",
            }
        },
    )
    slug = create_resp.json()["article"]["slug"]

    response = await test_client.put(
        f"{ARTICLES}/{slug}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated Title", "description": "After update"},
    )

    assert response.status_code == HTTP_200_OK
    data = response.json()["article"]
    assert data["description"] == "After update"


async def test_delete_article(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"del_{uid}", f"del_{uid}@test.com")
    token = await get_token_for_user(user)

    create_resp = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Delete Article {uid}",
                "description": "To delete",
                "body": "Delete body",
            }
        },
    )
    slug = create_resp.json()["article"]["slug"]

    response = await test_client.delete(
        f"{ARTICLES}/{slug}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    # Verify deleted
    get_resp = await test_client.get(f"{ARTICLES}/{slug}")
    assert get_resp.status_code == 404
