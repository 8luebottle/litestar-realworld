from litestar import Controller, post, get, delete
from app.schemas import Profile


class ProfileController(Controller):
    path = "api/profiles"

    @get(path="/{username:str}")
    async def get_profile(self) -> Profile:
        pass

    @post(path="/{username:str}/follow")
    async def follow_user(self) -> Profile:
        pass

    @delete(path="/{username:str}/follow")
    async def unfollow_user(self) -> Profile:
        pass
