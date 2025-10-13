from datetime import datetime

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Article
from app.schemas.request_schemas import (
    CreateArticleType,
    GetArticlesType,
    UpdateArticleType,
)

from .tag_queries import TagQueries


class ArticleQueries:
    @classmethod
    async def create_article(
        cls, user_id: str, article: CreateArticleType, session: AsyncSession
    ) -> Article:
        slug = slugify(article.title)
        created_at = datetime.now()

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
        return new_article

    @classmethod
    async def get_article_by_slug(
        cls, slug: str, session: AsyncSession
    ) -> Article | None:
        result = await session.execute(select(Article).where(Article.slug == slug))
        return result.unique().scalar_one_or_none()

    @classmethod
    async def get_articles(
        cls, query: GetArticlesType, id: str | None, session: AsyncSession
    ) -> list[Article]:
        pass

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
