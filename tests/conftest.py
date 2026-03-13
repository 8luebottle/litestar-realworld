from collections.abc import AsyncIterator
from uuid import uuid4

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture
from sqlalchemy.ext.asyncio import async_sessionmaker

from Conduit.auth.jwt_auth import jwt_auth
from Conduit.auth.password_helper import PasswordHelper
from Conduit.db.article_queries import ArticleQueries
from Conduit.db.comment_queries import CommentQueries
from Conduit.db.models import User
from Conduit.db.user_queries import UserQueries
from Conduit.main import app
from Conduit.schemas.request_schemas import (
    CommentBodyType,
    CommentType,
    CreateArticleType,
)


def unique_id() -> str:
    """테스트 데이터 격리를 위한 고유 ID 생성."""
    return uuid4().hex[:8]


async def create_user_in_db(
    username: str, email: str, password: str = "test_password"
) -> User:
    """DB에 직접 사용자를 생성하는 헬퍼 (Argon2 해싱 포함)."""
    sessionmaker = async_sessionmaker(expire_on_commit=False, bind=app.state.engine)
    pw_hash = PasswordHelper.hash(password)
    async with sessionmaker() as session:
        user = User(username=username, email=email, password=pw_hash, bio="")
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def get_token_for_user(user: User) -> str:
    """사용자의 JWT 토큰을 생성하는 헬퍼."""
    return jwt_auth.create_token(identifier=str(user.id))


@fixture(scope="session")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client


@fixture(scope="session")
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


@fixture(scope="session")
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


@fixture(scope="session")
async def author_token() -> str:
    sessionmaker = async_sessionmaker(expire_on_commit=False, bind=app.state.engine)
    async with sessionmaker() as session:
        author = await UserQueries.get_by_username("mock_author", session)
        if author is None:
            raise ValueError("`author_token` fixture could not find author")
        return jwt_auth.create_token(identifier=str(author.id))


@fixture(scope="session")
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
