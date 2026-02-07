from msgspec import Struct, field


class CreateArticleType(Struct):
    title: str
    description: str
    body: str
    tag_list: list[str] | None = field(default=None, name="tagList")


class CreateArticleWrapper(Struct):
    article: CreateArticleType


class UpdateArticleType(Struct):
    title: str | None = None
    description: str | None = None
    body: str | None = None


class CreateUserType(Struct):
    email: str
    username: str
    password: str


class CreateUserWrapper(Struct):
    user: CreateUserType


class LoginUserType(Struct):
    email: str
    password: str


class LoginWrapper(Struct):
    user: LoginUserType


class UpdateUserType(Struct):
    email: str | None = None
    username: str | None = None
    password: str | None = None
    image: str | None = None
    bio: str | None = None


class UpdateUserWrapper(Struct):
    user: UpdateUserType


class CommentBodyType(Struct):
    body: str


class CommentType(Struct):
    comment: CommentBodyType
