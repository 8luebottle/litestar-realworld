from uuid import UUID, uuid4

from litestar.exceptions import NotFoundException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.request_schemas import LoginUserType, UpdateUserType
from app.schemas.response_schemas import AuthenticatedUser


class UserQueries:
    @classmethod
    async def get(
        cls, user: LoginUserType, session: AsyncSession
    ) -> tuple[AuthenticatedUser, str]:
        query = select(User).where(
            User.email == user.email and User.password == user.password
        )
        result = await session.execute(query)
        try:
            authed_user = result.scalar_one()
            return (
                AuthenticatedUser(
                    email=authed_user.email,
                    username=authed_user.username,
                    bio=authed_user.bio,
                    image=authed_user.image,
                    token="dummy_token",
                ),
                str(authed_user.id),
            )
        except NoResultFound as e:
            raise NotFoundException(
                detail=f"User with {user.email=} and {user.password} not found."
            ) from e

    @classmethod
    async def get_by_id(cls, id: uuid4, session: AsyncSession) -> AuthenticatedUser:
        query = select(User).where(User.id == id)
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
            raise NotFoundException(detail=f"User with {id=} not found.") from e

    @classmethod
    async def get_user_by_id(cls, id: uuid4, session: AsyncSession) -> User:
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise NotFoundException(detail=f"User with {id=} not found.") from e

    @classmethod
    async def update(
        cls, id: str, user: UpdateUserType, session: AsyncSession
    ) -> AuthenticatedUser:
        user_to_update = await cls.get_user_by_id(UUID(id), session)

        if user.username is not None:
            user_to_update.username = user.username
        if user.email is not None:
            user_to_update.email = user.email
        if user.password is not None:
            user_to_update.password = user.password
        if user.bio is not None:
            user_to_update.bio = user.bio
        if user.image is not None:
            user_to_update.image = user.image

        await session.commit()

        updated_user = await cls.get_by_id(UUID(id), session)
        return AuthenticatedUser(
            email=updated_user.email,
            username=updated_user.username,
            bio=updated_user.bio,
            image=updated_user.image,
            token="dummy_token",
        )
