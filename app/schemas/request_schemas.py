from msgspec import Struct


class GetArticlesType(Struct):
    tag: str | None
    author: str | None
    favorited: str | None
    limit: int = 20
    offset: int = 0


class GetFeedType(Struct):
    limit: int = 20
    offset: int = 0


class CreateArticleType(Struct):
    title: str
    description: str
    body: str
    tag_list: list[str] | None


class UpdateArticleType(Struct):
    title: str | None
    description: str | None
    body: str | None


class CreateUserType(Struct):
    email: str
    username: str
    password: str


class LoginUserType(Struct):
    email: str
    password: str


class UpdateUserType(Struct):
    email: str | None
    username: str | None
    password: str | None
    image: str | None
    bio: str | None


class CommentBodyType(Struct):
    body: str


class CommentType(Struct):
    comment: CommentBodyType
