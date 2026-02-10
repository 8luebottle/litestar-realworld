from litestar import Litestar
from litestar.status_codes import HTTP_404_NOT_FOUND
from litestar.testing import AsyncTestClient

ENDPOINT = "/api/profiles"


async def test_get_profile_user_not_found(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.get(f"{ENDPOINT}/non-existent-user")

    assert response.status_code == HTTP_404_NOT_FOUND
