from datetime import timedelta
from typing import Any

from litestar import Controller, Request, get, post, put
from litestar.datastructures import State
from litestar.exceptions import HTTPException
from litestar.security.jwt import Token
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.auth.jwt_auth import ALGORITHM, SECRET, jwt_auth
from app.db.models import User
from app.db.user_queries import UserQueries
from app.schemas.request_schemas import (
    CreateUserWrapper,
    LoginWrapper,
    UpdateUserWrapper,
)
from app.schemas.response_schemas import AuthenticatedUserResponse, UserWrapper

sessionmaker = async_sessionmaker(expire_on_commit=False)


class UserController(Controller):
    path = "api"

    @post(
        path="/users", exclude_from_auth=True, response_model=AuthenticatedUserResponse
    )
    async def create_user(self, data: CreateUserWrapper, state: State) -> UserWrapper:
        data = data.user
        new_user = User(
            username=data.username, email=data.email, password=data.password, bio=""
        )
        async with sessionmaker(bind=state.engine) as session:
            try:
                async with session.begin():
                    session.add(new_user)
                    await session.flush()
            except IntegrityError:
                raise HTTPException(
                    "Username or email already in user", status_code=HTTP_409_CONFLICT
                )

        new_jwt = jwt_auth.create_token(
            identifier=str(new_user.id), token_expiration=timedelta(minutes=15)
        )

        user_response = AuthenticatedUserResponse(
            username=new_user.username,
            email=new_user.email,
            bio=new_user.bio,
            image=None,
            token=new_jwt,
        )
        return UserWrapper(user=user_response)

    @post(path="/users/login")
    async def login_user(self, data: LoginWrapper, state: State) -> UserWrapper:
        data = data.user
        async with sessionmaker(bind=state.engine) as session:
            user, id = await UserQueries.get(data, session)

        response = jwt_auth.login(id, send_token_as_response_body=True)
        user.token = response.content["token"]
        return UserWrapper(user=user)

    @get(path="/user")
    async def get_current_user(self, request: Request[User, Token, Any]) -> UserWrapper:
        user = AuthenticatedUserResponse(
            email=request.user.email,
            username=request.user.username,
            bio=request.user.bio,
            image=request.user.image,
            token=request.auth.encode(SECRET, ALGORITHM),
        )
        return UserWrapper(user=user)

    @put(path="/user")
    async def update_user(
        self, data: UpdateUserWrapper, request: Request[User, Token, Any], state: State
    ) -> UserWrapper:
        data = data.user
        async with sessionmaker(bind=state.engine) as session:
            updated_user = await UserQueries.update(request.auth.sub, data, session)
        updated_user.token = request.auth.encode(SECRET, ALGORITHM)
        return UserWrapper(user=updated_user)
