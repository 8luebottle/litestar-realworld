from litestar import Litestar
from litestar.status_codes import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from litestar.testing import AsyncTestClient

ENDPOINT = "/api/profiles"


async def test_get_profile_user_not_found(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get(f"{ENDPOINT}/non-existent-user")

    assert response.status_code == HTTP_404_NOT_FOUND


async def test_follow_user_no_token(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.post(f"{ENDPOINT}/non-existent-user/follow")

    assert response.status_code == HTTP_401_UNAUTHORIZED


async def test_follow_user_not_found(
    test_client: AsyncTestClient[Litestar], token: str
) -> None:
    response = await test_client.post(
        f"{ENDPOINT}/non-existent-user/follow",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_404_NOT_FOUND


async def test_unfollow_user_no_token(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.delete(f"{ENDPOINT}/non-existent-user/follow")

    assert response.status_code == HTTP_401_UNAUTHORIZED


async def test_unfollow_user_not_found(
    test_client: AsyncTestClient[Litestar], token: str
) -> None:
    response = await test_client.delete(
        f"{ENDPOINT}/non-existent-user/follow",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_404_NOT_FOUND
