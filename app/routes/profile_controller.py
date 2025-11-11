from typing import Any
from uuid import UUID

from litestar import Controller, Request, delete, get, post
from litestar.datastructures import State
from litestar.exceptions import NotFoundException
from litestar.security.jwt import Token
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import User
from app.db.user_queries import UserQueries
from app.schemas.response_schemas import ProfileResponse

sessionmaker = async_sessionmaker(expire_on_commit=False)


class ProfileController(Controller):
    path = "api/profiles"

    @get(path="/{username:str}", guards=[])
    async def get_profile(
        self, username: str, request: Request[User, Token, Any], state: State
    ) -> ProfileResponse:
        async with sessionmaker(bind=state.engine) as session:
            user = await UserQueries.get_by_username(username, session)
            if not user:
                raise NotFoundException(detail=f"No profile with {username=} found")

            if request.user:
                requester_id = UUID(request.user.id)
                is_following = await UserQueries.is_following(
                    requester_id, user.id, session
                )
            else:
                is_following = False

            return ProfileResponse(
                username=user.username,
                bio=user.bio,
                image=user.image,
                following=is_following,
            )

    @post(path="/{username:str}/follow")
    async def follow_user(self) -> ProfileResponse:
        pass

    @delete(path="/{username:str}/follow")
    async def unfollow_user(self) -> None:
        pass
