from app.schemas.request_schemas import CreateUserType, LoginUserType, UpdateUserType
from app.schemas.response_schemas import AuthenticatedUser
from sqlalchemy.ext.asyncio import AsyncSession


class UserQueries:
    @classmethod
    async def create(
        cls, user: CreateUserType, session: AsyncSession
    ) -> AuthenticatedUser:
        pass

    @classmethod
    async def get(cls, user: LoginUserType, session: AsyncSession) -> AuthenticatedUser:
        pass

    @classmethod
    async def update(
        cls, user: UpdateUserType, session: AsyncSession
    ) -> AuthenticatedUser:
        pass
