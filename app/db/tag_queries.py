from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ArticleTag, Tag


class TagQueries:
    @classmethod
    async def add_article_tags(
        cls, article_id: UUID, tags: list[str], session: AsyncSession
    ) -> None:
        for tag in tags:
            await cls.get_or_create_tag(tag, session)

        article_tags = [ArticleTag(article_id=article_id, tag=tag) for tag in tags]
        session.add_all(article_tags)
        await session.commit()

    @classmethod
    async def get_tag(cls, tag: str, session: AsyncSession) -> Tag | None:
        result = await session.execute(select(Tag).where(Tag.tag == tag))
        tag_found = result.scalar_one_or_none()
        if tag_found:
            return tag_found
        return None

    @classmethod
    async def get_or_create_tag(cls, tag: str, session: AsyncSession) -> Tag:
        result = await cls.get_tag(tag, session)
        if result:
            return result

        new_tag = Tag(tag=tag)
        session.add(new_tag)
        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            new_tag = await cls.get_tag(tag, session)
        return new_tag
