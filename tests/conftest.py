from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture
from sqlalchemy.ext.asyncio import async_sessionmaker

from Conduit.auth.jwt_auth import jwt_auth
from Conduit.db.article_queries import ArticleQueries
from Conduit.db.comment_queries import CommentQueries
from Conduit.db.models import Base, User
from Conduit.db.user_queries import UserQueries
from Conduit.main import app
from Conduit.schemas.request_schemas import (
    CommentBodyType,
    CommentType,
    CreateArticleType,
)


@fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client


@fixture(scope="function")
async def token() -> str:
    sessionmaker = async_sessionmaker(expire_on_commit=False, bind=app.state.engine)
    async with sessionmaker() as session:
        user = User(
            username="mock_user",
            email="mock@mock.com",
            password="mock_pw",
            bio="mock_bio",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return jwt_auth.create_token(identifier=str(user.id))


@fixture(scope="function")
async def article_slug() -> str:
    sessionmaker = async_sessionmaker(expire_on_commit=False, bind=app.state.engine)
    async with sessionmaker() as session:
        user = User(
            username="mock_author",
            email="author@mock.com",
            password="author_pw",
            bio="author_bio",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        article_to_create = CreateArticleType(
            title="mock article",
            description="mock description",
            body="mock body",
            tag_list=["mock tag"],
        )
        article = await ArticleQueries.create_article(
            str(user.id), article_to_create, session
        )
        return article.slug


@fixture(scope="function")
async def author_token() -> str:
    sessionmaker = async_sessionmaker(expire_on_commit=False, bind=app.state.engine)
    async with sessionmaker() as session:
        author = await UserQueries.get_by_username("mock_author", session)
        if author is None:
            raise ValueError("`author_token` fixture could not find author")
        return jwt_auth.create_token(identifier=str(author.id))


@fixture(scope="function")
async def comment_id() -> int:
    sessionmaker = async_sessionmaker(expire_on_commit=False, bind=app.state.engine)
    async with sessionmaker() as session:
        article = await ArticleQueries.get_article_by_slug("mock-article", session)
        if article is None:
            raise ValueError("`comment_id` fixture could not find article")

        author = await UserQueries.get_by_username("mock_author", session)
        if author is None:
            raise ValueError("`comment_id` fixture could not find author")

        comment_body = CommentType(CommentBodyType("mock comment"))
        comment = await CommentQueries.create_comment(
            comment_body, article.id, author.id, session
        )
        return comment.id


@fixture(scope="function", autouse=True)
async def clean_db() -> AsyncGenerator[Any, Any]:
    yield
    engine = app.state.engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
