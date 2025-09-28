from msgspec import Struct
from datetime import datetime


class User(Struct):
    email: str
    username: str
    bio: str
    image: str | None


class AuthenticatedUser(User):
    token: str


class Profile(Struct):
    username: str
    bio: str
    image: str | None
    following: bool


class Article(Struct):
    slug: str
    title: str
    description: str
    body: str
    tag_list: list[str]
    created_at: datetime
    updated_at: datetime
    favorited: bool
    favorites_count: int
    author: Profile


class ArticleList(Struct):
    articles: list[Article]
    articles_count: int


class Comment(Struct):
    id: int
    created_at: datetime
    updated_at: datetime
    body: str
    author: Profile


class CommentList(Struct):
    comments: list[Comment]


class TagList(Struct):
    tags: list[str]
