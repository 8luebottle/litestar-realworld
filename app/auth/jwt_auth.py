from uuid import UUID

from litestar import Request
from litestar.connection import ASGIConnection
from litestar.exceptions import NotFoundException
from litestar.security.jwt import JWTAuth, Token
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import User
from app.db.user_queries import UserQueries
from app.schemas.response_schemas import AuthenticatedUserResponse
from app.settings import settings


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection
) -> AuthenticatedUserResponse | None:
    state = connection.app.state
    sessionmaker = async_sessionmaker(expire_on_commit=False)
    async with sessionmaker(bind=state.engine) as session:
        try:
            user = await UserQueries.get_by_id(UUID(token.sub), session)
            return user
        except NotFoundException:
            return None


async def authenticate_manually(request: Request) -> User | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    try:
        token_str = auth_header[7:]
        token = Token.decode(
            token_str, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        state = request.app.state
        sessionmaker = async_sessionmaker(expire_on_commit=False)
        async with sessionmaker(bind=state.engine) as session:
            return await UserQueries.get_user_by_id(token.sub, session)
    except (KeyError, ValueError, NotFoundException):
        return None


jwt_auth = JWTAuth[User, Token](
    token_secret=settings.JWT_SECRET,
    retrieve_user_handler=retrieve_user_handler,
    exclude=["/schema", "/api/users", "api/users/login"],
)
