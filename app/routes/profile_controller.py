from typing import Any
from uuid import UUID

from litestar import Controller, Request, delete, get, post
from litestar.datastructures import State
from litestar.exceptions import NotFoundException
from litestar.security.jwt import Token
from litestar.status_codes import HTTP_200_OK
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.auth.jwt_auth import authenticate_manually
from app.db.models import User
from app.db.user_queries import UserQueries
from app.schemas.response_schemas import ProfileResponse, ProfileResponseWrapper

sessionmaker = async_sessionmaker(expire_on_commit=False)


class ProfileController(Controller):
    path = "api/profiles"

    @get(path="/{username:str}", exclude_from_auth=True)
    async def get_profile(
        self, username: str, request: Request[User, Token, Any], state: State
    ) -> ProfileResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            user = await UserQueries.get_by_username(username, session)
            if not user:
                raise NotFoundException(detail=f"No profile with {username=} found")

            requesting_user = await authenticate_manually(request)
            if requesting_user:
                is_following = await UserQueries.is_following(
                    requesting_user.id, user.id, session
                )
            else:
                is_following = False

            response = ProfileResponse(
                username=user.username,
                bio=user.bio,
                image=user.image,
                following=is_following,
            )
            return ProfileResponseWrapper(profile=response)

    @post(path="/{username:str}/follow", status_code=HTTP_200_OK)
    async def follow_user(
        self, username: str, request: Request[User, Token, Any], state: State
    ) -> ProfileResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            follower_id = request.auth.sub
            followed_id = await UserQueries.get_by_username(username, session)
            if not followed_id:
                raise NotFoundException(f"No user with {username=} found")

            await UserQueries.follow_user(UUID(follower_id), followed_id.id, session)
            username = followed_id.username
            bio = followed_id.bio
            image = followed_id.image
        response = ProfileResponse(
            username=username, bio=bio, image=image, following=True
        )
        return ProfileResponseWrapper(response)

    @delete(path="/{username:str}/follow", status_code=HTTP_200_OK)
    async def unfollow_user(
        self, username: str, request: Request[User, Token, Any], state: State
    ) -> ProfileResponseWrapper:
        async with sessionmaker(bind=state.engine) as session:
            follower_id = request.auth.sub
            followed_user = await UserQueries.get_by_username(username, session)
            if not followed_user:
                raise NotFoundException(f"No user with {username=} found")

            await UserQueries.delete_user(UUID(follower_id), followed_user.id, session)
            await session.refresh(followed_user)
            username = followed_user.username
            bio = followed_user.bio
            image = followed_user.image
        response = ProfileResponse(
            username=username, bio=bio, image=image, following=False
        )
        return ProfileResponseWrapper(response)
