from datetime import datetime
from uuid import UUID

from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_404_NOT_FOUND
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Article, ArticleTag, UserFavorite, UserFollow
from app.schemas.request_schemas import (
    CreateArticleType,
    GetArticlesType,
    GetFeedType,
    UpdateArticleType,
)

from .tag_queries import TagQueries
from .user_queries import UserQueries


class ArticleQueries:
    @classmethod
    async def create_article(
        cls, user_id: str, article: CreateArticleType, session: AsyncSession
    ) -> Article:
        created_at = datetime.now()
        slug = slugify(article.title)
        if await cls.get_article_by_slug(slug, session) is not None:
            slug = "".join([slug, created_at])

        new_article = Article(
            slug=slug,
            title=article.title,
            description=article.description,
            body=article.body,
            created_at=created_at,
            updated_at=created_at,
            author=user_id,
        )

        session.add(new_article)
        await session.flush()

        if article.tag_list:
            article.tag_list = list(set(article.tag_list))
            await TagQueries.add_article_tags(new_article.id, article.tag_list, session)

        await session.refresh(new_article)
        await session.commit()
        return new_article

    @classmethod
    async def get_article_by_slug(
        cls, slug: str, session: AsyncSession
    ) -> Article | None:
        result = await session.execute(select(Article).where(Article.slug == slug))
        return result.unique().scalar_one_or_none()

    @classmethod
    async def get_articles(
        cls, query: GetArticlesType, session: AsyncSession
    ) -> list[Article]:
        stmt = select(Article).order_by(Article.created_at.desc())

        if query.tag:
            stmt = stmt.join(Article.article_tags)
            stmt = stmt.where(ArticleTag.tag == query.tag)
        if query.author:
            author = await UserQueries.get_by_username(query.author, session)
            if not author:
                raise NotFoundException(
                    "Author id not found", status_code=HTTP_404_NOT_FOUND
                )
            stmt = stmt.where(Article.author == author.id)
        if query.favorited:
            favorited = await UserQueries.get_by_username(query.favorited, session)
            if not favorited:
                raise NotFoundException(
                    "Favorited id not found", status_code=HTTP_404_NOT_FOUND
                )
            stmt = stmt.join(Article.favorites)
            stmt = stmt.where(UserFavorite.user_id == favorited.id)

        stmt = stmt.offset(query.offset).limit(query.limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_article_feed(
        cls, query: GetFeedType, user_id: UUID, session: AsyncSession
    ) -> list[Article]:
        stmt = (
            select(Article)
            .join(UserFollow, Article.author == UserFollow.followed_user_id)
            .where(UserFollow.follower_user_id == user_id)
            .order_by(Article.created_at.desc())
            .offset(query.offset)
            .limit(query.limit)
        )

        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def update_article(
        cls, slug: str, updates: UpdateArticleType, session: AsyncSession
    ) -> Article:
        article_to_update = await cls.get_article_by_slug(slug, session)

        new_slug = article_to_update.slug
        if updates.title is not None:
            new_slug = slugify(updates.title)
            article_to_update.slug = new_slug
            article_to_update.title = updates.title
        if updates.description is not None:
            article_to_update.description = updates.description
        if updates.body is not None:
            article_to_update.body = updates.body

        if any([updates.title, updates.description, updates.body]):
            article_to_update.updated_at = datetime.now()

        await session.commit()
        await session.refresh(article_to_update)
        return article_to_update

    @classmethod
    async def delete_article(cls, slug: str, session: AsyncSession) -> None:
        article_to_delete = await session.scalar(
            select(Article).where(Article.slug == slug)
        )
        await session.delete(article_to_delete)
        await session.commit()
        return
