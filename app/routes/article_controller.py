from typing import Any
from uuid import UUID

from litestar import Controller, Request, delete, get, post, put
from litestar.datastructures import State
from litestar.exceptions import NotFoundException
from litestar.security.jwt import Token
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.article_queries import ArticleQueries
from app.db.models import User
from app.db.user_queries import UserQueries
from app.schemas.request_schemas import (
    CreateArticleType,
    GetArticlesType,
    GetFeedType,
    UpdateArticleType,
)
from app.schemas.response_schemas import (
    ArticleListResponse,
    ArticleResponse,
    CommentListResponse,
    CommentResponse,
    ProfileResponse,
)

sessionmaker = async_sessionmaker(expire_on_commit=False)


class ArticleController(Controller):
    path = "api/articles"

    @get()
    async def get_articles(self, query: GetArticlesType) -> ArticleListResponse:
        pass

    @get(path="/feed")
    async def get_article_feed(self, query: GetFeedType) -> ArticleListResponse:
        pass

    @get(path="/{slug:str}", exclude_from_auth=True)
    async def get_article(self, slug: str, state: State) -> ArticleResponse:
        # TODO: determine if authentication is present or not
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            tags = [tag.tag for tag in article.article_tags]
            author = await UserQueries.get_by_id(article.author, session)
            profile = ProfileResponse(
                username=author.username,
                bio=author.bio,
                image=author.image,
                following=False,  # TODO: true if author follows themselves, otherwise false.
            )

            return ArticleResponse(
                slug=article.slug,
                title=article.title,
                description=article.description,
                body=article.body,
                tag_list=tags,
                created_at=article.created_at,
                updated_at=article.updated_at,
                favorited=False,
                favorites_count=0,
                author=profile,
            )

    @post()
    async def create_article(
        self, data: CreateArticleType, request: Request[User, Token, Any], state: State
    ) -> ArticleResponse:
        async with sessionmaker(bind=state.engine) as session:
            new_article = await ArticleQueries.create_article(
                request.auth.sub, data, session
            )
            tags = [tag.tag for tag in new_article.article_tags]
            author = await UserQueries.get_by_id(UUID(request.auth.sub), session)
            profile = ProfileResponse(
                username=author.username,
                bio=author.bio,
                image=author.image,
                following=True,  # TODO: true if author follows themselves, otherwise false.
            )

            article_to_return = ArticleResponse(
                slug=new_article.slug,
                title=new_article.title,
                description=new_article.description,
                body=new_article.body,
                tag_list=tags,
                created_at=new_article.created_at,
                updated_at=new_article.updated_at,
                favorited=False,
                favorites_count=0,
                author=profile,
            )

        return article_to_return

    @put(path="/{slug:str}")
    async def update_article(self, data: UpdateArticleType) -> ArticleResponse:
        pass

    @delete(path="/{slug:str}")
    async def delete_article(self) -> None:
        pass

    @post(path="/{slug:str}/comments")
    async def add_comment(self) -> CommentResponse:
        pass

    @get(path="/{slug:str}/comments")
    async def get_comments(self) -> CommentListResponse:
        pass

    @delete(path="/{slug:str}/comments/{id:int}")
    async def delete_comment(self) -> None:
        pass

    @post(path="/{slug:str}/favorite")
    async def favorite_article(self) -> ArticleResponse:
        pass

    @delete(path="/{slug:str}/favorite")
    async def unfavorite_article(self) -> None:
        pass
