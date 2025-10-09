from datetime import timedelta

from litestar import Controller, get, post, put
from litestar.datastructures import State
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.auth.jwt_auth import jwt_auth
from app.db.models import User
from app.db.queries import UserQueries
from app.schemas.request_schemas import CreateUserType, LoginUserType, UpdateUserType
from app.schemas.response_schemas import AuthenticatedUser

sessionmaker = async_sessionmaker(expire_on_commit=False)


class UserController(Controller):
    path = "api"

    @post(path="/users", exclude_from_auth=True, response_model=AuthenticatedUser)
    async def create_user(
        self, data: CreateUserType, state: State
    ) -> AuthenticatedUser:
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

        return AuthenticatedUser(
            username=new_user.username,
            email=new_user.email,
            bio=new_user.bio,
            image=None,
            token=new_jwt,
        )

    @post(path="/users/login")
    async def login_user(self, data: LoginUserType, state: State) -> AuthenticatedUser:
        async with sessionmaker(bind=state.engine) as session:
            user = await UserQueries.get(data, session)
            return user

    @get(path="/user")
    async def get_current_usert(self) -> AuthenticatedUser:
        pass

    @put(path="/user")
    async def update_user(self, data: UpdateUserType) -> AuthenticatedUser:
        pass
