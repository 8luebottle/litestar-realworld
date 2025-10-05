from app.schemas.request_schemas import CreateUserType, LoginUserType, UpdateUserType
from app.schemas.response_schemas import AuthenticatedUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User
from sqlalchemy.exc import NoResultFound
from litestar.exceptions import NotFoundException


class UserQueries:
    @classmethod
    async def create(
        cls, user: CreateUserType, session: AsyncSession
    ) -> AuthenticatedUser:
        pass

    @classmethod
    async def get(cls, user: LoginUserType, session: AsyncSession) -> AuthenticatedUser:
        query = select(User).where(
            User.email == user.email and User.password == user.password
        )
        result = await session.execute(query)
        try:
            authed_user = result.scalar_one()
            return AuthenticatedUser(
                email=authed_user.email,
                username=authed_user.username,
                bio=authed_user.bio,
                image=authed_user.image,
                token="dummy_token",
            )
        except NoResultFound as e:
            raise NotFoundException(
                detail=f"User with {user.email=} and {user.password} not found."
            ) from e

    @classmethod
    async def update(
        cls, user: UpdateUserType, session: AsyncSession
    ) -> AuthenticatedUser:
        pass
