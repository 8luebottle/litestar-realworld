from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Article
from app.schemas.request_schemas import (
    CreateArticleType,
    GetArticlesType,
    UpdateArticleType,
)


class ArticleQueries:
    @classmethod
    def create_article(
        cls, id: str, article: CreateArticleType, session: AsyncSession
    ) -> Article:
        pass

    @classmethod
    def get_article_by_slug(cls, slug: str, session: AsyncSession) -> Article:
        pass

    @classmethod
    def get_articles(
        cls, query: GetArticlesType, id: str | None, session: AsyncSession
    ) -> list[Article]:
        pass

    @classmethod
    def update_article(
        cls, slug: str, updates: UpdateArticleType, session: AsyncSession
    ) -> Article:
        pass

    @classmethod
    def delete_article(cls, slug: str, session: AsyncSession) -> None:
        pass
