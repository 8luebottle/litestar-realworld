from litestar import Controller, post, get, put
from litestar.datastructures import State
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.schemas.response_schemas import AuthenticatedUser
from app.schemas.request_schemas import CreateUserType, LoginUserType, UpdateUserType
from app.db.models import User


sessionmaker = async_sessionmaker(expire_on_commit=False)


class UserController(Controller):
    path = "api"

    @post(path="/users")
    async def create_user(
        self, data: CreateUserType, state: State
    ) -> AuthenticatedUser:
        new_user = User(
            username=data.username, email=data.email, password=data.password, bio=""
        )
        async with sessionmaker(bind=state.engine) as session:
            async with session.begin():
                session.add(new_user)
        return AuthenticatedUser(
            username=new_user.username,
            email=new_user.email,
            bio=new_user.bio,
            image=None,
            token="dummy_token",
        )

    @post(path="/users/login")
    async def login_user(self, data: LoginUserType) -> AuthenticatedUser:
        pass

    @get(path="/user")
    async def get_current_usert(self) -> AuthenticatedUser:
        pass

    @put(path="/user")
    async def update_user(self, data: UpdateUserType) -> AuthenticatedUser:
        pass
