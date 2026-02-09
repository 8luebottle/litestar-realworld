from typing import Any

import pytest
from litestar import Litestar
from litestar.status_codes import (
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
