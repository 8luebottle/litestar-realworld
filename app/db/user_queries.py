from uuid import UUID

from litestar.exceptions import NotFoundException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, UserFollow
from app.schemas.request_schemas import LoginUserType, UpdateUserType
from app.schemas.response_schemas import AuthenticatedUserResponse


class UserQueries:
    @classmethod
    async def get(
        cls, user: LoginUserType, session: AsyncSession
    ) -> tuple[AuthenticatedUserResponse, str]:
        query = select(User).where(
            User.email == user.email and User.password == user.password
        )
        result = await session.execute(query)
        try:
            authed_user = result.scalar_one()
            return (
                AuthenticatedUserResponse(
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
    async def get_by_id(
        cls, id: UUID, session: AsyncSession
    ) -> AuthenticatedUserResponse:
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        try:
            authed_user = result.scalar_one()
            return AuthenticatedUserResponse(
                email=authed_user.email,
                username=authed_user.username,
                bio=authed_user.bio,
                image=authed_user.image,
                token="dummy_token",
            )
        except NoResultFound as e:
            raise NotFoundException(detail=f"User with {id=} not found.") from e

    @classmethod
    async def get_user_by_id(cls, id: UUID, session: AsyncSession) -> User:
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise NotFoundException(detail=f"User with {id=} not found.") from e

    @classmethod
    async def get_by_username(cls, username: str, session: AsyncSession) -> User | None:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update(
        cls, id: str, user: UpdateUserType, session: AsyncSession
    ) -> AuthenticatedUserResponse:
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
        return AuthenticatedUserResponse(
            email=updated_user.email,
            username=updated_user.username,
            bio=updated_user.bio,
            image=updated_user.image,
            token="dummy_token",
        )

    @classmethod
    async def is_following(
        cls, follower_id: UUID, followed_id: UUID, session: AsyncSession
    ) -> bool:
        follower = await cls.get_by_id(follower_id, session)
        followed = await cls.get_by_id(followed_id, session)

        if not follower or not followed:
            return False

        query = select(UserFollow).where(
            UserFollow.followed_user_id == followed_id,
            UserFollow.follower_user_id == follower_id,
        )
        result = await session.execute(query)
        is_following = True if result.scalar_one_or_none() else False
        return is_following

    @classmethod
    async def follow_user(
        cls, follower_id: UUID, followed_id: UUID, session: AsyncSession
    ) -> None:
        existing = await session.execute(
            select(UserFollow).where(
                UserFollow.follower_user_id == follower_id,
                UserFollow.followed_user_id == followed_id,
            )
        )
        if existing.scalar_one_or_none():
            return

        new_follow = UserFollow(
            follower_user_id=follower_id, followed_user_id=followed_id
        )
        session.add(new_follow)
        await session.commit()
