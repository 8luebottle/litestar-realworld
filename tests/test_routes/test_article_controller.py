import pytest

from litestar import Litestar
from litestar.testing import AsyncTestClient
from litestar.status_codes import HTTP_404_NOT_FOUND


async def test_get_article_feed_no_token(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.get("/api/feed")

    assert response.status_code == HTTP_404_NOT_FOUND
