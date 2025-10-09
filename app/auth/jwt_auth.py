from litestar.connection import ASGIConnection
from litestar.exceptions import NotFoundException, PermissionDeniedException
from litestar.security.jwt import JWTAuth, Token
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import User
from app.db.queries import UserQueries

SECRET = "dummy-secret"


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User:
    state = connection.app.state
    sessionmaker = async_sessionmaker(expire_on_commit=False)
    async with sessionmaker(bind=state.engine) as session:
        try:
            user = await UserQueries.get_by_id(token.sub, session)
            return user
        except NotFoundException:
            raise PermissionDeniedException()


jwt_auth = JWTAuth[User, Token](
    token_secret=SECRET,
    retrieve_user_handler=retrieve_user_handler,
)
