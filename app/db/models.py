from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100))  # TODO: needs to be unique
    password: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(String(200))
    image: Mapped[str | None] = mapped_column(String(100))

    comments: Mapped[set["Comment"]] = relationship()
    followers: Mapped[list["UserFollow"]] = relationship(
        "UserFollow",
        foreign_keys="UserFollow.followed_user_id",
        back_populates="followed_user",
    )
    following: Mapped[list["UserFollow"]] = relationship(
        "UserFollow",
        foreign_keys="UserFollow.follower_user_id",
        back_populates="follower_user",
    )


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    slug: Mapped[str] = mapped_column(String(150))
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(250))
    body: Mapped[str] = mapped_column(String(10_000))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    author: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    comments: Mapped[set["Comment"]] = relationship()
    article_tags: Mapped[set["ArticleTag"]] = relationship(lazy="joined")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    body: Mapped[str] = mapped_column(String(500))
    article_id: Mapped[UUID] = mapped_column(ForeignKey("articles.id"))
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))


class Tag(Base):
    __tablename__ = "tags"

    tag: Mapped[str] = mapped_column(String(30), primary_key=True)

    article_tags: Mapped[set["ArticleTag"]] = relationship()


class ArticleTag(Base):
    __tablename__ = "article_tags"

    article_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id"), primary_key=True
    )
    tag: Mapped[str] = mapped_column(
        String(30), ForeignKey("tags.tag"), primary_key=True
    )


class UserFavorite(Base):
    __tablename__ = "user_favorites"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    article_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id"), primary_key=True
    )


class UserFollow(Base):
    __tablename__ = "user_follows"

    followed_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    follower_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )

    followed_user: Mapped["User"] = relationship(
        "User", foreign_keys=[followed_user_id], back_populates="followers"
    )
    follower_user: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_user_id], back_populates="following"
    )
