from datetime import datetime

from msgspec import Struct


class UserResponse(Struct):
    email: str
    username: str
    bio: str
    image: str | None


class AuthenticatedUserResponse(UserResponse):
    token: str


class UserWrapper(Struct):
    user: AuthenticatedUserResponse


class ProfileResponse(Struct):
    username: str
    bio: str
    image: str | None
    following: bool


class ArticleResponse(Struct, rename="camel"):
    slug: str
    title: str
    description: str
    body: str
    tag_list: list[str]
    created_at: datetime
    updated_at: datetime
    favorited: bool
    favorites_count: int
    author: ProfileResponse


class ArticleResponseWrapper(Struct):
    article: ArticleResponse


class ArticleListResponse(Struct, rename="camel"):
    articles: list[ArticleResponse]
    articles_count: int


class CommentResponse(Struct, rename="camel"):
    id: int
    created_at: datetime
    updated_at: datetime
    body: str
    author: ProfileResponse


class CommentResponseWrapper(Struct):
    comment: CommentResponse


class CommentListResponse(Struct):
    comments: list[CommentResponse]


class TagListResponse(Struct):
    tags: list[str]
