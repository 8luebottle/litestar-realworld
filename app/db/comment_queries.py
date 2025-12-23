from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Comment
from app.schemas.request_schemas import CommentType


class CommentQueries:
    @classmethod
    async def create_comment(
        cls,
        comment: CommentType,
        article_id: UUID,
        user_id: UUID,
        session: AsyncSession,
    ) -> Comment:
        created_at = datetime.now()
        new_comment = Comment(
            created_at=created_at,
            updated_at=created_at,
            body=comment.comment.body,
            article_id=article_id,
            author_id=user_id,
        )
        session.add(new_comment)
        await session.flush()
        await session.refresh(new_comment)
        await session.commit()

        return new_comment

    @classmethod
    async def get_comments(
        cls, article_id: UUID, session: AsyncSession
    ) -> list[Comment]:
        comments = await session.execute(
            select(Comment).where(Comment.article_id == article_id)
        )
        return comments.scalars().all()

    @classmethod
    async def get_comment_by_id(cls, comment_id: int, session: AsyncSession) -> Comment:
        comment = await session.execute(select(Comment).where(Comment.id == comment_id))
        return comment.scalar_one_or_none()

    @classmethod
    async def delete_comment(cls, comment_id: int, session: AsyncSession) -> None:
        comment_to_delete = await cls.get_comment_by_id(comment_id, session)
        await session.delete(comment_to_delete)
        await session.commit()
        return
