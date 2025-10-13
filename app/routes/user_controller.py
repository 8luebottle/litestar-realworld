from datetime import timedelta
from typing import Any

from litestar import Controller, Request, get, post, put
from litestar.datastructures import State
from litestar.security.jwt import Token
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.auth.jwt_auth import ALGORITHM, SECRET, jwt_auth
from app.db.models import User
from app.db.user_queries import UserQueries
from app.schemas.request_schemas import CreateUserType, LoginUserType, UpdateUserType
from app.schemas.response_schemas import AuthenticatedUserResponse

sessionmaker = async_sessionmaker(expire_on_commit=False)


class UserController(Controller):
    path = "api"

    @post(
        path="/users", exclude_from_auth=True, response_model=AuthenticatedUserResponse
    )
    async def create_user(
        self, data: CreateUserType, state: State
    ) -> AuthenticatedUserResponse:
        new_user = User(
            username=data.username, email=data.email, password=data.password, bio=""
        )
        async with sessionmaker(bind=state.engine) as session:
            async with session.begin():
                session.add(new_user)
                await session.flush()

        new_jwt = jwt_auth.create_token(
            identifier=str(new_user.id), token_expiration=timedelta(minutes=15)
        )

        return AuthenticatedUserResponse(
            username=new_user.username,
            email=new_user.email,
            bio=new_user.bio,
            image=None,
            token=new_jwt,
        )

    @post(path="/users/login")
    async def login_user(
        self, data: LoginUserType, state: State
    ) -> AuthenticatedUserResponse:
        async with sessionmaker(bind=state.engine) as session:
            user, id = await UserQueries.get(data, session)

        response = jwt_auth.login(id, send_token_as_response_body=True)
        user.token = response.content["token"]
        return user

    @get(path="/user")
    async def get_current_user(
        self, request: Request[User, Token, Any]
    ) -> AuthenticatedUserResponse:
        return AuthenticatedUserResponse(
            email=request.user.email,
            username=request.user.username,
            bio=request.user.bio,
            image=request.user.image,
            token=request.auth.encode(SECRET, ALGORITHM),
        )

    @put(path="/user")
    async def update_user(
        self, data: UpdateUserType, request: Request[User, Token, Any], state: State
    ) -> AuthenticatedUserResponse:
        async with sessionmaker(bind=state.engine) as session:
            updated_user = await UserQueries.update(request.auth.sub, data, session)
        updated_user.token = request.auth.encode(SECRET, ALGORITHM)
        return updated_user
