from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserFavorite


class FavoriteQueries:
    @classmethod
    async def create_favorite(
        cls, article_id: UUID, user_id: UUID, session: AsyncSession
    ) -> UserFavorite:
        new_favorite = UserFavorite(user_id=user_id, article_id=article_id)
        session.add(new_favorite)
        await session.commit()

        return new_favorite

    @classmethod
    async def get_favorite(
        cls, article_id: UUID, user_id: UUID, session: AsyncSession
    ) -> UserFavorite | None:
        result = await session.execute(
            select(UserFavorite).where(
                UserFavorite.article_id == article_id
                and UserFavorite.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_favorite_by_id(
        cls, favorite_id: UUID, session: AsyncSession
    ) -> UserFavorite | None:
        result = await session.execute(
            select(UserFavorite).where(UserFavorite.id == favorite_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_favorites_count(cls, article_id: UUID, session: AsyncSession) -> int:
        result = await session.scalar(
            select(func.count())
            .select_from(UserFavorite)
            .filter(UserFavorite.article_id == article_id)
        )
        count = result if result else 0
        return count

    @classmethod
    async def delete_favorite(
        cls, article_id: UUID, user_id: UUID, session: AsyncSession
    ) -> None:
        favorite_to_delete = await cls.get_favorite(article_id, user_id, session)
        if not favorite_to_delete:
            return
        await session.delete(favorite_to_delete)
        await session.commit()
        return
