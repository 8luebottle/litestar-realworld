"""Tag controller tests — OpenSpec tags 스펙 기반."""

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from tests.conftest import create_user_in_db, get_token_for_user, unique_id

TAGS = "/api/tags"
ARTICLES = "/api/articles"


async def test_get_tags(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.get(TAGS)

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert "tags" in data
    assert isinstance(data["tags"], list)


async def test_get_tags_includes_article_tags(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"tag_{uid}", f"tag_{uid}@test.com")
    token = await get_token_for_user(user)
    tag_name = f"testtag{uid}"

    # Create article with a unique tag
    await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Tag Article {uid}",
                "description": "Tag test",
                "body": "Body",
                "tagList": [tag_name],
            }
        },
    )

    response = await test_client.get(TAGS)

    assert response.status_code == HTTP_200_OK
    assert tag_name in response.json()["tags"]


async def test_get_articles_filter_by_tag(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"ftag_{uid}", f"ftag_{uid}@test.com")
    token = await get_token_for_user(user)
    tag_name = f"filtertag{uid}"

    await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Filter Tag {uid}",
                "description": "Filter by tag",
                "body": "Body",
                "tagList": [tag_name],
            }
        },
    )

    response = await test_client.get(f"{ARTICLES}?tag={tag_name}")

    assert response.status_code == HTTP_200_OK
    articles = response.json()["articles"]
    assert len(articles) >= 1
    assert tag_name in articles[0]["tagList"]
