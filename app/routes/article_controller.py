from typing import Any
from uuid import UUID

from litestar import Controller, Request, delete, get, post, put
from litestar.datastructures import State
from litestar.exceptions import HTTPException, NotAuthorizedException, NotFoundException
from litestar.security.jwt import Token
from litestar.status_codes import HTTP_200_OK, HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.auth.jwt_auth import authenticate_manually
from app.db.article_queries import ArticleQueries
from app.db.comment_queries import CommentQueries
from app.db.favorite_queries import FavoriteQueries
from app.db.models import Article, User
from app.db.user_queries import UserQueries
from app.schemas.request_schemas import (
    CommentType,
    CreateArticleWrapper,
    GetArticlesType,
    GetFeedType,
    UpdateArticleType,
)
from app.schemas.response_schemas import (
    ArticleListResponse,
    ArticleNoBodyResponse,
    ArticleResponse,
    ArticleResponseWrapper,
    CommentListResponse,
    CommentResponse,
    CommentResponseWrapper,
    ProfileResponse,
)

sessionmaker = async_sessionmaker(expire_on_commit=False)


class ArticleController(Controller):
    path = "/api/articles"

    async def _make_article_no_body_response(
        self,
        article: Article,
        request: Request[User, Token, Any],
        session: AsyncSession,
    ) -> ArticleNoBodyResponse:
        tags = [tag.tag for tag in article.article_tags]
        tags.sort()
        author = await UserQueries.get_by_id(article.author, session)

        is_following, is_favorited = False, False
        requesting_user = await authenticate_manually(request)
        if requesting_user:
            is_following = await UserQueries.is_following(
                requesting_user.id, author.id, session
            )
            favorite = await FavoriteQueries.get_favorite(
                article.id, requesting_user.id, session
            )
            is_favorited = True if favorite else False
        profile = ProfileResponse(
            username=author.username,
            bio=author.bio,
            image=author.image,
            following=is_following,
        )
        favorites_count = await FavoriteQueries.get_favorites_count(article.id, session)

        return ArticleNoBodyResponse(
            slug=article.slug,
            title=article.title,
            description=article.description,
            tag_list=tags,
            created_at=article.created_at,
            updated_at=article.updated_at,
            favorited=is_favorited,
            favorites_count=favorites_count,
            author=profile,
        )

    async def _make_article_response(
        self,
        article: Article,
        request: Request[User, Token, Any],
        session: AsyncSession,
    ) -> ArticleResponse:
        article_no_body = await self._make_article_no_body_response(
            article, request, session
        )
        return ArticleResponse(
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            tag_list=article_no_body.tag_list,
            created_at=article.created_at,
            updated_at=article.updated_at,
            favorited=article_no_body.favorited,
            favorites_count=article_no_body.favorites_count,
            author=article_no_body.author,
        )

    @get(exclude_from_auth=True)
    async def get_articles(
        self, query: GetArticlesType, request: Request[User, Token, Any], state: State
    ) -> ArticleListResponse:
        async with sessionmaker(bind=state.engine) as session:
            articles = await ArticleQueries.get_articles(query, session)
            article_response = [
                await self._make_article_no_body_response(article, request, session)
                for article in articles
            ]
            return ArticleListResponse(article_response, len(article_response))

    @get(path="/feed")
    async def get_article_feed(
        self, query: GetFeedType, request: Request[User, Token, Any], state: State
    ) -> ArticleListResponse:
        async with sessionmaker(bind=state.engine) as session:
            user_id = UUID(request.auth.sub)
            articles = await ArticleQueries.get_article_feed(query, user_id, session)
            article_response = [
                await self._make_article_no_body_response(article, request, session)
                for article in articles
            ]
            return ArticleListResponse(article_response, len(article_response))

    @get(path="/{slug:str}", exclude_from_auth=True)
    async def get_article(
        self, slug: str, request: Request[User, Token, Any], state: State
    ) -> ArticleResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            response = await self._make_article_response(article, request, session)
            return ArticleResponseWrapper(article=response)

    @post()
    async def create_article(
        self,
        data: CreateArticleWrapper,
        request: Request[User, Token, Any],
        state: State,
    ) -> ArticleResponseWrapper:
        article_data = data.article
        async with sessionmaker(bind=state.engine) as session:
            new_article = await ArticleQueries.create_article(
                request.auth.sub, article_data, session
            )
            tags = [tag.tag for tag in new_article.article_tags]
            author = await UserQueries.get_by_id(UUID(request.auth.sub), session)
            is_following = await UserQueries.is_following(author.id, author.id, session)
            profile = ProfileResponse(
                username=author.username,
                bio=author.bio,
                image=author.image,
                following=is_following,
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

        return ArticleResponseWrapper(article=article_to_return)

    @put(path="/{slug:str}")
    async def update_article(
        self,
        slug: str,
        data: UpdateArticleType,
        request: Request[User, Token, Any],
        state: State,
    ) -> ArticleResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            if str(article.author) != request.auth.sub:
                raise NotAuthorizedException("User not authorized to update article")

            updated_article = await ArticleQueries.update_article(slug, data, session)
            response = await self._make_article_response(
                updated_article, request, session
            )
            return ArticleResponseWrapper(article=response)

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
    ) -> CommentResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")
            new_comment = await CommentQueries.create_comment(
                data, article.id, UUID(request.auth.sub), session
            )
            author_profile = await UserQueries.get_by_id(new_comment.author_id, session)
            is_following = await UserQueries.is_following(
                author_profile.id, author_profile.id, session
            )
            profile = ProfileResponse(
                username=author_profile.username,
                bio=author_profile.bio,
                image=author_profile.image,
                following=is_following,
            )
            response = CommentResponse(
                id=new_comment.id,
                created_at=new_comment.created_at,
                updated_at=new_comment.updated_at,
                body=new_comment.body,
                author=profile,
            )
            return CommentResponseWrapper(comment=response)

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
                requesting_user = await authenticate_manually(request)
                if requesting_user:
                    is_following = await UserQueries.is_following(
                        requesting_user.id, id, session
                    )
                else:
                    is_following = False
                profiles[id] = ProfileResponse(
                    username=author_profile.username,
                    bio=author_profile.bio,
                    image=author_profile.image,
                    following=is_following,
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
    async def delete_comment(
        self, slug: str, id: int, request: Request[User, Token, Any], state: State
    ) -> None:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")

            comment = await CommentQueries.get_comment_by_id(id, session)
            if comment is None:
                raise NotFoundException(f"No comment with {id=} found")

            if str(comment.author_id) != request.auth.sub:
                raise NotAuthorizedException("Only commenter can delete their comment")

            await CommentQueries.delete_comment(id, session)

    @post(path="/{slug:str}/favorite")
    async def favorite_article(
        self, slug: str, request: Request[User, Token, Any], state: State
    ) -> ArticleResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")

            try:
                _ = await FavoriteQueries.create_favorite(
                    article.id, UUID(request.auth.sub), session
                )
            except IntegrityError:
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail="Could not favorite article due to pre-existing favorite or other",
                )

            tags = [tag.tag for tag in article.article_tags]
            author = await UserQueries.get_by_id(article.author, session)
            is_following = await UserQueries.is_following(
                UUID(request.auth.sub), author.id, session
            )
            profile = ProfileResponse(
                username=author.username,
                bio=author.bio,
                image=author.image,
                following=is_following,
            )
            favorites_count = await FavoriteQueries.get_favorites_count(
                article.id, session
            )

            response = ArticleResponse(
                slug=article.slug,
                title=article.title,
                description=article.description,
                body=article.body,
                tag_list=tags,
                created_at=article.created_at,
                updated_at=article.updated_at,
                favorited=True,
                favorites_count=favorites_count,
                author=profile,
            )
            return ArticleResponseWrapper(article=response)

    @delete(path="/{slug:str}/favorite", status_code=HTTP_200_OK)
    async def unfavorite_article(
        self, slug: str, request: Request[User, Token, Any], state: State
    ) -> ArticleResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            article = await ArticleQueries.get_article_by_slug(slug, session)
            if article is None:
                raise NotFoundException(f"No article with {slug=} found")

            _ = await FavoriteQueries.delete_favorite(
                article.id, UUID(request.auth.sub), session
            )
            await session.refresh(article)
            response = await self._make_article_response(article, request, session)
            return ArticleResponseWrapper(article=response)
