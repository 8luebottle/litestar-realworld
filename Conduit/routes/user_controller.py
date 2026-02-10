from datetime import timedelta
from typing import Any

from litestar import Controller, Request, get, post, put
from litestar.datastructures import State
from litestar.exceptions import HTTPException, NotFoundException
from litestar.security.jwt import Token
from litestar.status_codes import HTTP_422_UNPROCESSABLE_ENTITY
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from Conduit.auth.jwt_auth import jwt_auth
from Conduit.auth.password_helper import PasswordHelper
from Conduit.db.models import User
from Conduit.db.user_queries import UserQueries
from Conduit.schemas.request_schemas import (
    CreateUserWrapper,
    LoginWrapper,
    UpdateUserType,
    UpdateUserWrapper,
)
from Conduit.schemas.response_schemas import AuthenticatedUserResponse, UserWrapper
from Conduit.settings import settings

sessionmaker = async_sessionmaker(expire_on_commit=False)


class UserController(Controller):
    path = "/api"

    @post(
        path="/users", exclude_from_auth=True, response_model=AuthenticatedUserResponse
    )
    async def create_user(self, data: CreateUserWrapper, state: State) -> UserWrapper:
        async with sessionmaker(bind=state.engine) as session:
            user_with_email = await UserQueries.get_by_email(data.user.email, session)
            user_with_username = await UserQueries.get_by_username(
                data.user.username, session
            )
            if user_with_email is not None or user_with_username is not None:
                raise HTTPException(
                    "Username or email already in use",
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                )

        pw_hash = PasswordHelper.hash(data.user.password)
        new_user = User(
            username=data.user.username,
            email=data.user.email,
            password=pw_hash,
            bio="",
        )
        async with sessionmaker(bind=state.engine) as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

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
        async with sessionmaker(bind=state.engine) as session:
            user = await UserQueries.get_by_email(data.user.email, session)

        exception_str = f"User with email: '{data.user.email}' and password: '{data.user.password}' not found"
        if user is None:
            raise NotFoundException(exception_str)

        is_pw_correct = PasswordHelper.verify(user.password, data.user.password)
        if not is_pw_correct:
            raise NotFoundException(exception_str)

        is_rehash_needed = PasswordHelper.is_rehash_needed(user.password)
        if is_rehash_needed:
            rehashed_pw = PasswordHelper.hash(data.user.password)
            updated_password = UpdateUserType(password=rehashed_pw)
            async with sessionmaker(bind=state.engine) as session:
                user = await UserQueries.update(str(user.id), updated_password, session)

        response = jwt_auth.login(str(user.id), send_token_as_response_body=True)
        user_data = AuthenticatedUserResponse(
            email=user.email,
            username=user.username,
            bio=user.bio,
            image=user.image,
            token=response.content["token"],
        )
        return UserWrapper(user=user_data)

    @get(path="/user")
    async def get_current_user(self, request: Request[User, Token, Any]) -> UserWrapper:
        user = AuthenticatedUserResponse(
            email=request.user.email,
            username=request.user.username,
            bio=request.user.bio,
            image=request.user.image,
            token=request.auth.encode(settings.JWT_SECRET, settings.JWT_ALGORITHM),
        )
        return UserWrapper(user=user)

    @put(path="/user")
    async def update_user(
        self, data: UpdateUserWrapper, request: Request[User, Token, Any], state: State
    ) -> UserWrapper:
        async with sessionmaker(bind=state.engine) as session:
            try:
                updated_user = await UserQueries.update(
                    request.auth.sub, data.user, session
                )
            except IntegrityError:
                error_str = "Cannot use a username or email that is already in use"
                raise HTTPException(detail=error_str, status_code=422)
        updated_token = request.auth.encode(settings.JWT_SECRET, settings.JWT_ALGORITHM)
        user_data = AuthenticatedUserResponse(
            email=updated_user.email,
            username=updated_user.username,
            bio=updated_user.bio,
            image=updated_user.image,
            token=updated_token,
        )
        return UserWrapper(user=user_data)
