from litestar import Controller, post, get, put
from app.schemas import AuthenticatedUser


class UserController(Controller):
    path = "api"

    @post(path="/users")
    async def create_user(
        self, email: str, username: str, password: str
    ) -> AuthenticatedUser:
        pass

    @post(path="/users/login")
    async def login_user(self, email: str, password: str) -> AuthenticatedUser:
        pass

    @get(path="/user")
    async def get_current_usert(self) -> AuthenticatedUser:
        pass

    @put(path="/user")
    async def update_user(
        self,
        email: str | None,
        username: str | None,
        password: str | None,
        image: str | None,
        bio: str | None,
    ) -> AuthenticatedUser:
        pass
