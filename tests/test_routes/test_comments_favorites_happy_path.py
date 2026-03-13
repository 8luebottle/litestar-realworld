"""Comments & Favorites happy path tests — OpenSpec comments-and-favorites 스펙 기반."""

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.testing import AsyncTestClient

from tests.conftest import create_user_in_db, get_token_for_user, unique_id

ARTICLES = "/api/articles"


async def _create_article(test_client: AsyncTestClient, token: str, uid: str) -> str:
    """테스트용 글 생성 후 slug 반환."""
    resp = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"CF Article {uid}",
                "description": "For comments/favorites test",
                "body": "Body content",
            }
        },
    )
    return resp.json()["article"]["slug"]


async def test_add_comment(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"cmnt_{uid}", f"cmnt_{uid}@test.com")
    token = await get_token_for_user(user)
    slug = await _create_article(test_client, token, uid)

    response = await test_client.post(
        f"{ARTICLES}/{slug}/comments",
        headers={"Authorization": f"Bearer {token}"},
        json={"comment": {"body": "Great article!"}},
    )

    assert response.status_code == HTTP_201_CREATED
    data = response.json()["comment"]
    assert data["body"] == "Great article!"
    assert data["author"]["username"] == f"cmnt_{uid}"
    assert "id" in data
    assert "createdAt" in data


async def test_get_comments(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"gcmt_{uid}", f"gcmt_{uid}@test.com")
    token = await get_token_for_user(user)
    slug = await _create_article(test_client, token, uid)

    # Add a comment
    await test_client.post(
        f"{ARTICLES}/{slug}/comments",
        headers={"Authorization": f"Bearer {token}"},
        json={"comment": {"body": "Comment 1"}},
    )

    response = await test_client.get(f"{ARTICLES}/{slug}/comments")

    assert response.status_code == HTTP_200_OK
    comments = response.json()["comments"]
    assert len(comments) >= 1
    assert comments[0]["body"] == "Comment 1"


async def test_get_comments_empty(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"ecmt_{uid}", f"ecmt_{uid}@test.com")
    token = await get_token_for_user(user)
    slug = await _create_article(test_client, token, uid)

    response = await test_client.get(f"{ARTICLES}/{slug}/comments")

    assert response.status_code == HTTP_200_OK
    assert response.json()["comments"] == []


async def test_delete_comment(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"dcmt_{uid}", f"dcmt_{uid}@test.com")
    token = await get_token_for_user(user)
    slug = await _create_article(test_client, token, uid)

    # Create comment
    comment_resp = await test_client.post(
        f"{ARTICLES}/{slug}/comments",
        headers={"Authorization": f"Bearer {token}"},
        json={"comment": {"body": "To delete"}},
    )
    comment_id = comment_resp.json()["comment"]["id"]

    # Delete comment
    response = await test_client.delete(
        f"{ARTICLES}/{slug}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_204_NO_CONTENT


async def test_favorite_article(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    author = await create_user_in_db(f"favau_{uid}", f"favau_{uid}@test.com")
    reader = await create_user_in_db(f"favrd_{uid}", f"favrd_{uid}@test.com")
    author_token = await get_token_for_user(author)
    reader_token = await get_token_for_user(reader)
    slug = await _create_article(test_client, author_token, uid)

    response = await test_client.post(
        f"{ARTICLES}/{slug}/favorite",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    assert response.status_code == HTTP_201_CREATED
    data = response.json()["article"]
    assert data["favorited"] is True
    assert data["favoritesCount"] >= 1


async def test_unfavorite_article(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    author = await create_user_in_db(f"ufau_{uid}", f"ufau_{uid}@test.com")
    reader = await create_user_in_db(f"ufrd_{uid}", f"ufrd_{uid}@test.com")
    author_token = await get_token_for_user(author)
    reader_token = await get_token_for_user(reader)
    slug = await _create_article(test_client, author_token, uid)

    # Favorite first
    await test_client.post(
        f"{ARTICLES}/{slug}/favorite",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    # Then unfavorite
    response = await test_client.delete(
        f"{ARTICLES}/{slug}/favorite",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    assert response.status_code == HTTP_200_OK
    data = response.json()["article"]
    assert data["favorited"] is False


async def test_get_articles_filter_by_favorited(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    author = await create_user_in_db(f"ffau_{uid}", f"ffau_{uid}@test.com")
    reader = await create_user_in_db(f"ffrd_{uid}", f"ffrd_{uid}@test.com")
    author_token = await get_token_for_user(author)
    reader_token = await get_token_for_user(reader)
    slug = await _create_article(test_client, author_token, uid)

    # Favorite the article
    await test_client.post(
        f"{ARTICLES}/{slug}/favorite",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    response = await test_client.get(f"{ARTICLES}?favorited=ffrd_{uid}")

    assert response.status_code == HTTP_200_OK
    articles = response.json()["articles"]
    assert len(articles) >= 1
