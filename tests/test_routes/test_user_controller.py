from typing import Any

import pytest
from litestar import Litestar
from litestar.status_codes import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from litestar.testing import AsyncTestClient

USERS = "/api/users"
USER = "/api/user"


@pytest.mark.parametrize(
    "email,username",
    [("mock@mock.com", "not in use"), ("not_in_use@mock.com", "mock_user")],
)
async def test_create_user_username_email_in_user(
    email: str, username: str, test_client: AsyncTestClient, token: str
) -> None:
    new_user = {"user": {"email": email, "username": username, "password": "mock_pw"}}

    response = await test_client.post(f"{USERS}", json=new_user)

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert (
        str(response.content, "utf-8")
        == '{"status_code":422,"detail":"Username or email already in use"}'
    )


@pytest.mark.parametrize(
    "body,expected",
    [
        ({}, "{'errors': {'data': 'Object missing required field `user`'}}"),
        ({"user": {}}, "{'errors': {'user': 'Object missing required field `email`'}}"),
        (
            {"user": {"email": "eml@mock.com", "username": "usr"}},
            "{'errors': {'user': 'Object missing required field `password`'}}",
        ),
        (
            {"user": {"email": "eml@mock.com", "password": "pw"}},
            "{'errors': {'user': 'Object missing required field `username`'}}",
        ),
        (
            {"user": {"username": "usr", "password": "pw"}},
            "{'errors': {'user': 'Object missing required field `email`'}}",
        ),
    ],
)
async def test_create_user_invalid_request(
    body: dict[str, Any], expected: str, test_client: AsyncTestClient[Litestar]
) -> None:
    response = await test_client.post(f"{USERS}", json=body)

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert str(response.content, "utf-8") == expected


@pytest.mark.parametrize(
    "body,expected",
    [
        ({}, "{'errors': {'data': 'Object missing required field `user`'}}"),
        ({"user": {}}, "{'errors': {'user': 'Object missing required field `email`'}}"),
        (
            {"user": {"email": ""}},
            "{'errors': {'user': 'Object missing required field `password`'}}",
        ),
        (
            {"user": {"password": ""}},
            "{'errors': {'user': 'Object missing required field `email`'}}",
        ),
    ],
)
async def test_user_login_invalid_request(
    body: dict[str, Any], expected: str, test_client: AsyncTestClient[Litestar]
) -> None:
    response = await test_client.post(f"{USERS}/login", json=body)

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert str(response.content, "utf-8") == expected


@pytest.mark.parametrize(
    "body,expected",
    [
        (
            {"user": {"email": "not_used@mock.com", "password": "mock_pw"}},
            '{"status_code":404,"detail":"User with email: \'not_used@mock.com\' and password: \'mock_pw\' not found"}',
        ),
        (
            {"user": {"email": "mock@mock.com", "password": "wrong_pass"}},
            '{"status_code":404,"detail":"User with email: \'mock@mock.com\' and password: \'wrong_pass\' not found"}',
        ),
    ],
)
async def test_user_login_not_found(
    body: dict[str, Any], expected: str, test_client: AsyncTestClient
) -> None:
    response = await test_client.post(f"{USERS}/login", json=body)

    assert response.status_code == HTTP_404_NOT_FOUND
    assert str(response.content, "utf-8") == expected


async def test_get_current_user_no_token(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get(f"{USER}")

    assert response.status_code == HTTP_401_UNAUTHORIZED


async def test_update_user_no_token(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.put(f"{USER}")

    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "body,expected",
    [
        ({}, "{'errors': {'data': 'Object missing required field `user`'}}"),
        (
            {"user": {"email": 1}},
            "{'errors': {'user.email': 'Expected `str | null`, got `int`'}}",
        ),
        (
            {"user": {"username": "mock_author"}},
            '{"status_code":422,"detail":"Cannot use a username or email that is already in use"}',
        ),
        (
            {"user": {"email": "author@mock.com"}},
            '{"status_code":422,"detail":"Cannot use a username or email that is already in use"}',
        ),
        (
            {"user": {"username": "mock_author", "email": "author@mock.com"}},
            '{"status_code":422,"detail":"Cannot use a username or email that is already in use"}',
        ),
    ],
)
async def test_update_user_invalid_request(
    body: dict[str, Any],
    expected: str,
    test_client: AsyncTestClient[Litestar],
    token: str,
    article_slug: str,
    author_token: str,
) -> None:
    response = await test_client.put(
        f"{USER}",
        headers={"Authorization": f"Bearer {token}"},
        json=body,
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert str(response.content, "utf-8") == expected
