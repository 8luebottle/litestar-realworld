from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Comment
from app.schemas.request_schemas import CommentType


class CommentQueries:
    @classmethod
    def create_comment(
        cls, comment: CommentType, article_id: UUID, session: AsyncSession
    ) -> Comment:
        pass

    @classmethod
    def get_comments(cls, article_id: UUID, session: AsyncSession) -> list[Comment]:
        pass

    @classmethod
    def delete_comment(cls, comment_id: int, session: AsyncSession) -> None:
        pass
