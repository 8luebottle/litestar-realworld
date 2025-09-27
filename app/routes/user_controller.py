from litestar import Controller, post, get, put
from app.schemas import AuthenticatedUser


class UserController(Controller):
    path = "api"

    @post(path="/users")
    def create_user(email: str, username: str, password: str) -> AuthenticatedUser:
        pass

    @post(path="/users/login")
    def login_user(email: str, password: str) -> AuthenticatedUser:
        pass

    @get(path="/user")
    def get_current_usert() -> AuthenticatedUser:
        pass

    @put(path="/user")
    def update_user(
        email: str | None,
        username: str | None,
        password: str | None,
        image: str | None,
        bio: str | None,
    ) -> AuthenticatedUser:
        pass
