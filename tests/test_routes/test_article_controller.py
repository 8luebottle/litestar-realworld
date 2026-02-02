from litestar import Litestar
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from litestar.testing import AsyncTestClient, RequestFactory


# async def test_get_article_feed_no_token(
#     test_client: AsyncTestClient[Litestar],
# ) -> None:
#     response = await test_client.get("/api/feed")

#     assert response.status_code == HTTP_404_NOT_FOUND


async def test_get_article_feed_invalid_request(
    authed_test_client: AsyncTestClient[Litestar],
) -> None:    
    response = await authed_test_client.get("/api/feed/")

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
