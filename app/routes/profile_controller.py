from litestar import Controller, post, get, delete
from app.schemas import Profile


class ProfileController(Controller):
    path = "api/profiles"

    @get(path="/{username:str}")
    def get_profile() -> Profile:
        pass

    @post(path="/{username:str}/follow")
    def follow_user() -> Profile:
        pass

    @delete(path="/{username:str}/follow")
    def unfollow_user() -> Profile:
        pass
