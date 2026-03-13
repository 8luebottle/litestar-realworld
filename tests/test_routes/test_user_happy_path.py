"""User controller happy path tests — OpenSpec user-auth 스펙 기반."""

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from tests.conftest import create_user_in_db, get_token_for_user, unique_id

USERS = "/api/users"
USER = "/api/user"


async def test_create_user_success(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    new_user = {
        "user": {
            "email": f"{uid}@test.com",
            "username": f"user_{uid}",
            "password": "secure_password",
        }
    }

    response = await test_client.post(USERS, json=new_user)

    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == f"{uid}@test.com"
    assert data["user"]["username"] == f"user_{uid}"
    assert data["user"]["bio"] == ""
    assert data["user"]["image"] is None
    assert "token" in data["user"]


async def test_login_success(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    password = "login_test_pw"
    await create_user_in_db(f"login_{uid}", f"login_{uid}@test.com", password)

    response = await test_client.post(
        f"{USERS}/login",
        json={"user": {"email": f"login_{uid}@test.com", "password": password}},
    )

    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    assert data["user"]["email"] == f"login_{uid}@test.com"
    assert data["user"]["username"] == f"login_{uid}"
    assert "token" in data["user"]


async def test_get_current_user(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"current_{uid}", f"current_{uid}@test.com")
    token = await get_token_for_user(user)

    response = await test_client.get(USER, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["user"]["username"] == f"current_{uid}"
    assert data["user"]["email"] == f"current_{uid}@test.com"
    assert "token" in data["user"]


async def test_update_user_success(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"update_{uid}", f"update_{uid}@test.com")
    token = await get_token_for_user(user)

    response = await test_client.put(
        USER,
        headers={"Authorization": f"Bearer {token}"},
        json={"user": {"bio": "updated bio", "image": "https://img.test/avatar.png"}},
    )

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["user"]["bio"] == "updated bio"
    assert data["user"]["image"] == "https://img.test/avatar.png"
    assert data["user"]["username"] == f"update_{uid}"


async def test_update_user_email(test_client: AsyncTestClient[Litestar]) -> None:
    uid = unique_id()
    user = await create_user_in_db(f"updeml_{uid}", f"updeml_{uid}@test.com")
    token = await get_token_for_user(user)
    new_email = f"new_{uid}@test.com"

    response = await test_client.put(
        USER,
        headers={"Authorization": f"Bearer {token}"},
        json={"user": {"email": new_email}},
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["user"]["email"] == new_email
