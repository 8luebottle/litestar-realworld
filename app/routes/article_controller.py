from typing import Any
from uuid import UUID

from litestar import Controller, Request, delete, get, post, put
from litestar.datastructures import State
from litestar.exceptions import NotAuthorizedException, NotFoundException
from litestar.security.jwt import Token
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.article_queries import ArticleQueries
from app.db.comment_queries import CommentQueries
from app.db.models import User
from app.db.user_queries import UserQueries
from app.schemas.request_schemas import (
    CommentType,
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
    async def update_article(
        self,
        slug: str,
        data: UpdateArticleType,
        request: Request[User, Token, Any],
        state: State,
    ) -> ArticleResponse:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            if str(article.author) != request.auth.sub:
                raise NotAuthorizedException("User not authorized to update article")

            updated_article = await ArticleQueries.update_article(slug, data, session)
            tags = [tag.tag for tag in updated_article.article_tags]
            author = await UserQueries.get_by_id(UUID(request.auth.sub), session)
            profile = ProfileResponse(
                username=author.username,
                bio=author.bio,
                image=author.image,
                following=True,  # TODO: true if author follows themselves, otherwise false.
            )

            return ArticleResponse(
                slug=updated_article.slug,
                title=updated_article.title,
                description=updated_article.description,
                body=updated_article.body,
                tag_list=tags,
                created_at=updated_article.created_at,
                updated_at=updated_article.updated_at,
                favorited=False,  # TODO: true if author follows themselves, otherwise false.
                favorites_count=0,  # TODO: true if author favorited this article.
                author=profile,
            )

    @delete(path="/{slug:str}")
    async def delete_article(
        self, slug: str, request: Request[User, Token, Any], state: State
    ) -> None:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            if str(article.author) != request.auth.sub:
                raise NotAuthorizedException("User not authorized to delete article")

            await ArticleQueries.delete_article(slug, session)
        return

    @post(path="/{slug:str}/comments")
    async def add_comment(
        self,
        slug: str,
        data: CommentType,
        request: Request[User, Token, Any],
        state: State,
    ) -> CommentResponse:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            new_comment = await CommentQueries.create_comment(
                data, article.id, UUID(request.auth.sub), session
            )
            author_profile = await UserQueries.get_by_id(new_comment.author_id, session)
            profile = ProfileResponse(
                username=author_profile.username,
                bio=author_profile.bio,
                image=author_profile.image,
                following=False,  # TODO: true if commenter follows themselves
            )
            return CommentResponse(
                id=new_comment.id,
                created_at=new_comment.created_at,
                updated_at=new_comment.updated_at,
                body=new_comment.body,
                author=profile,
            )

    @get(path="/{slug:str}/comments", exclude_from_auth=True)
    async def get_comments(
        self, slug: str, request: Request[User, Token, Any], state: State
    ) -> CommentListResponse:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            comments = await CommentQueries.get_comments(article.id, session)

            if comments == []:
                return CommentListResponse(comments=[])
            user_ids = set([comment.author_id for comment in comments])
            profiles = {}
            for id in user_ids:
                author_profile = await UserQueries.get_by_id(id, session)
                profiles[id] = ProfileResponse(
                    username=author_profile.username,
                    bio=author_profile.bio,
                    image=author_profile.image,
                    following=False,  # TODO: true if getter follows author
                )
            comments_to_return = [
                CommentResponse(
                    id=comment.id,
                    created_at=comment.created_at,
                    updated_at=comment.updated_at,
                    body=comment.body,
                    author=profiles[comment.author_id],
                )
                for comment in comments
            ]
            return CommentListResponse(comments=comments_to_return)

    @delete(path="/{slug:str}/comments/{id:int}")
    async def delete_comment(self) -> None:
        pass

    @post(path="/{slug:str}/favorite")
    async def favorite_article(self) -> ArticleResponse:
        pass

    @delete(path="/{slug:str}/favorite")
    async def unfavorite_article(self) -> None:
        pass
