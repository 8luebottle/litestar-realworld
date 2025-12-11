from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100))  # TODO: needs to be unique
    password: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(String(200))
    image: Mapped[str | None] = mapped_column(String(100))

    comments: Mapped[set["Comment"]] = relationship(cascade="all, delete-orphan")
    favorites: Mapped[set["UserFavorite"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan"
    )
    followers: Mapped[list["UserFollow"]] = relationship(
        foreign_keys="[UserFollow.followed_user_id]",
        back_populates="followed_user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    following: Mapped[list["UserFollow"]] = relationship(
        foreign_keys="[UserFollow.follower_user_id]",
        back_populates="follower_user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("username", name="_username_uc"),
        UniqueConstraint("email", name="_email_uc"),
    )


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    slug: Mapped[str] = mapped_column(String(150), unique=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(250))
    body: Mapped[str] = mapped_column(String(10_000))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    author: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), ForeignKey("users.id"))

    comments: Mapped[set["Comment"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan"
    )
    article_tags: Mapped[set["ArticleTag"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan"
    )
    favorites: Mapped[set["UserFavorite"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    body: Mapped[str] = mapped_column(String(500))
    article_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE")
    )
    author_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )


class Tag(Base):
    __tablename__ = "tags"

    tag: Mapped[str] = mapped_column(String(30), primary_key=True)

    article_tags: Mapped[set["ArticleTag"]] = relationship()


class ArticleTag(Base):
    __tablename__ = "article_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE")
    )
    tag: Mapped[str] = mapped_column(String(30), ForeignKey("tags.tag"))


class UserFavorite(Base):
    __tablename__ = "user_favorites"

    id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    article_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE")
    )

    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="_user_article_uc"),
    )


class UserFollow(Base):
    __tablename__ = "user_follows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    followed_user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    follower_user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )

    followed_user: Mapped["User"] = relationship(
        foreign_keys=[followed_user_id], back_populates="followers"
    )
    follower_user: Mapped["User"] = relationship(
        foreign_keys=[follower_user_id], back_populates="following"
    )

    __table_args__ = (
        UniqueConstraint(
            "followed_user_id", "follower_user_id", name="_user_follow_uc"
        ),
    )
