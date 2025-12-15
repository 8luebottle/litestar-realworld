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


class ArticleResponse(Struct):
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


class ArticleListResponse(Struct):
    articles: list[ArticleResponse]
    articles_count: int


class CommentResponse(Struct):
    id: int
    created_at: datetime
    updated_at: datetime
    body: str
    author: ProfileResponse


class CommentListResponse(Struct):
    comments: list[CommentResponse]


class TagListResponse(Struct):
    tags: list[str]
