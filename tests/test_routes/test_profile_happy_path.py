"""Profile controller happy path tests — OpenSpec profiles 스펙 기반."""

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from tests.conftest import create_user_in_db, get_token_for_user, unique_id

PROFILES = "/api/profiles"


async def test_get_profile_unauthenticated(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    await create_user_in_db(f"prof_{uid}", f"prof_{uid}@test.com")

    response = await test_client.get(f"{PROFILES}/prof_{uid}")

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["profile"]["username"] == f"prof_{uid}"
    assert data["profile"]["following"] is False


async def test_get_profile_authenticated_not_following(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    viewer = await create_user_in_db(f"viewer_{uid}", f"viewer_{uid}@test.com")
    await create_user_in_db(f"target_{uid}", f"target_{uid}@test.com")
    token = await get_token_for_user(viewer)

    response = await test_client.get(
        f"{PROFILES}/target_{uid}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["profile"]["following"] is False


async def test_follow_user(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    follower = await create_user_in_db(f"flwr_{uid}", f"flwr_{uid}@test.com")
    await create_user_in_db(f"flwd_{uid}", f"flwd_{uid}@test.com")
    token = await get_token_for_user(follower)

    response = await test_client.post(
        f"{PROFILES}/flwd_{uid}/follow",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["profile"]["username"] == f"flwd_{uid}"
    assert response.json()["profile"]["following"] is True


async def test_follow_then_get_profile_shows_following(
    test_client: AsyncTestClient[Litestar],
) -> None:
    uid = unique_id()
    follower = await create_user_in_db(f"fgp_{uid}", f"fgp_{uid}@test.com")
    await create_user_in_db(f"fgpt_{uid}", f"fgpt_{uid}@test.com")
    token = await get_token_for_user(follower)

    await test_client.post(
        f"{PROFILES}/fgpt_{uid}/follow",
        headers={"Authorization": f"Bearer {token}"},
    )

    response = await test_client.get(
        f"{PROFILES}/fgpt_{uid}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["profile"]["following"] is True


async def test_unfollow_user(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    follower = await create_user_in_db(f"uf_{uid}", f"uf_{uid}@test.com")
    await create_user_in_db(f"uft_{uid}", f"uft_{uid}@test.com")
    token = await get_token_for_user(follower)

    # Follow first
    await test_client.post(
        f"{PROFILES}/uft_{uid}/follow",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then unfollow
    response = await test_client.delete(
        f"{PROFILES}/uft_{uid}/follow",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["profile"]["following"] is False
