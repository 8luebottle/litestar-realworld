from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Comment
from app.schemas.request_schemas import CommentType


class CommentQueries:
    @classmethod
    async def create_comment(
        cls, comment: CommentType, article_id: UUID, user_id: UUID, session: AsyncSession
    ) -> Comment:
        new_comment = Comment(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            body=comment.comment.body,
            article_id=article_id,
            author_id=user_id,
        )
        session.add(new_comment)
        await session.commit()

        return new_comment


    @classmethod
    async def get_comments(cls, article_id: UUID, session: AsyncSession) -> list[Comment]:
        pass

    @classmethod
    async def delete_comment(cls, comment_id: int, session: AsyncSession) -> None:
        pass
