from litestar import Controller, post, get, put
from app.schemas.response_schemas import AuthenticatedUser
from app.schemas.request_schemas import CreateUserType, LoginUserType, UpdateUserType


class UserController(Controller):
    path = "api"

    @post(path="/users")
    async def create_user(self, data: CreateUserType) -> AuthenticatedUser:
        pass

    @post(path="/users/login")
    async def login_user(self, data: LoginUserType) -> AuthenticatedUser:
        pass

    @get(path="/user")
    async def get_current_usert(self) -> AuthenticatedUser:
        pass

    @put(path="/user")
    async def update_user(self, data: UpdateUserType) -> AuthenticatedUser:
        pass
