"""E2E tests — 핵심 사용자 시나리오를 처음부터 끝까지 검증."""

from litestar import Litestar
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from litestar.testing import AsyncTestClient

from tests.conftest import unique_id

USERS = "/api/users"
USER = "/api/user"
ARTICLES = "/api/articles"
PROFILES = "/api/profiles"
TAGS = "/api/tags"


async def test_full_user_lifecycle(test_client: AsyncTestClient[Litestar]) -> None:
    """사용자 등록 → 로그인 → 프로필 조회 → 업데이트 전체 흐름."""
    uid = unique_id()

    # 1. Register
    reg_resp = await test_client.post(
        USERS,
        json={
            "user": {
                "email": f"e2e_{uid}@test.com",
                "username": f"e2e_{uid}",
                "password": "e2e_password",
            }
        },
    )
    assert reg_resp.status_code == HTTP_201_CREATED
    token = reg_resp.json()["user"]["token"]

    # 2. Login
    login_resp = await test_client.post(
        f"{USERS}/login",
        json={"user": {"email": f"e2e_{uid}@test.com", "password": "e2e_password"}},
    )
    assert login_resp.status_code == HTTP_201_CREATED
    token = login_resp.json()["user"]["token"]

    # 3. Get current user
    me_resp = await test_client.get(USER, headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == HTTP_200_OK
    assert me_resp.json()["user"]["username"] == f"e2e_{uid}"

    # 4. Update profile
    update_resp = await test_client.put(
        USER,
        headers={"Authorization": f"Bearer {token}"},
        json={"user": {"bio": "E2E test bio"}},
    )
    assert update_resp.status_code == HTTP_200_OK
    assert update_resp.json()["user"]["bio"] == "E2E test bio"


async def test_article_publish_and_interact(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """글 작성 → 댓글 → 즐겨찾기 → 피드 확인 전체 흐름."""
    uid = unique_id()

    # Setup: Create author and reader
    author_resp = await test_client.post(
        USERS,
        json={
            "user": {
                "email": f"author_e2e_{uid}@test.com",
                "username": f"author_e2e_{uid}",
                "password": "author_pw",
            }
        },
    )
    author_token = author_resp.json()["user"]["token"]

    reader_resp = await test_client.post(
        USERS,
        json={
            "user": {
                "email": f"reader_e2e_{uid}@test.com",
                "username": f"reader_e2e_{uid}",
                "password": "reader_pw",
            }
        },
    )
    reader_token = reader_resp.json()["user"]["token"]

    # 1. Author creates article with tags
    create_resp = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {author_token}"},
        json={
            "article": {
                "title": f"E2E Article {uid}",
                "description": "E2E test article",
                "body": "Full article body for E2E testing",
                "tagList": [f"e2e{uid}", "testing"],
            }
        },
    )
    assert create_resp.status_code == HTTP_201_CREATED
    slug = create_resp.json()["article"]["slug"]

    # 2. Reader follows author
    follow_resp = await test_client.post(
        f"{PROFILES}/author_e2e_{uid}/follow",
        headers={"Authorization": f"Bearer {reader_token}"},
    )
    assert follow_resp.status_code == HTTP_200_OK
    assert follow_resp.json()["profile"]["following"] is True

    # 3. Article appears in reader's feed
    feed_resp = await test_client.get(
        f"{ARTICLES}/feed",
        headers={"Authorization": f"Bearer {reader_token}"},
    )
    assert feed_resp.status_code == HTTP_200_OK
    feed_slugs = [a["slug"] for a in feed_resp.json()["articles"]]
    assert slug in feed_slugs

    # 4. Reader adds comment
    comment_resp = await test_client.post(
        f"{ARTICLES}/{slug}/comments",
        headers={"Authorization": f"Bearer {reader_token}"},
        json={"comment": {"body": "Great E2E article!"}},
    )
    assert comment_resp.status_code == HTTP_201_CREATED
    comment_id = comment_resp.json()["comment"]["id"]

    # 5. Reader favorites article
    fav_resp = await test_client.post(
        f"{ARTICLES}/{slug}/favorite",
        headers={"Authorization": f"Bearer {reader_token}"},
    )
    assert fav_resp.status_code == HTTP_201_CREATED
    assert fav_resp.json()["article"]["favorited"] is True
    assert fav_resp.json()["article"]["favoritesCount"] == 1

    # 6. Verify article shows in favorited filter
    fav_list_resp = await test_client.get(f"{ARTICLES}?favorited=reader_e2e_{uid}")
    assert fav_list_resp.status_code == HTTP_200_OK
    assert len(fav_list_resp.json()["articles"]) >= 1

    # 7. Tags appear in tag list
    tags_resp = await test_client.get(TAGS)
    assert tags_resp.status_code == HTTP_200_OK
    assert f"e2e{uid}" in tags_resp.json()["tags"]

    # 8. Reader unfavorites and deletes comment
    unfav_resp = await test_client.delete(
        f"{ARTICLES}/{slug}/favorite",
        headers={"Authorization": f"Bearer {reader_token}"},
    )
    assert unfav_resp.status_code == HTTP_200_OK
    assert unfav_resp.json()["article"]["favorited"] is False

    del_comment_resp = await test_client.delete(
        f"{ARTICLES}/{slug}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {reader_token}"},
    )
    assert del_comment_resp.status_code == HTTP_204_NO_CONTENT

    # 9. Author deletes article
    del_resp = await test_client.delete(
        f"{ARTICLES}/{slug}",
        headers={"Authorization": f"Bearer {author_token}"},
    )
    assert del_resp.status_code == HTTP_204_NO_CONTENT

    # 10. Article no longer exists
    get_resp = await test_client.get(f"{ARTICLES}/{slug}")
    assert get_resp.status_code == 404


async def test_article_update_flow(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """글 작성 → 수정 → 조회하여 수정 반영 확인."""
    uid = unique_id()

    reg_resp = await test_client.post(
        USERS,
        json={
            "user": {
                "email": f"upd_e2e_{uid}@test.com",
                "username": f"upd_e2e_{uid}",
                "password": "upd_pw",
            }
        },
    )
    token = reg_resp.json()["user"]["token"]

    # Create
    create_resp = await test_client.post(
        ARTICLES,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "article": {
                "title": f"Update E2E {uid}",
                "description": "Before",
                "body": "Original body",
            }
        },
    )
    slug = create_resp.json()["article"]["slug"]

    # Update
    update_resp = await test_client.put(
        f"{ARTICLES}/{slug}",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "After update", "body": "Updated body"},
    )
    assert update_resp.status_code == HTTP_200_OK

    # Verify
    get_resp = await test_client.get(f"{ARTICLES}/{slug}")
    assert get_resp.status_code == HTTP_200_OK
    article = get_resp.json()["article"]
    assert article["description"] == "After update"
    assert article["body"] == "Updated body"
