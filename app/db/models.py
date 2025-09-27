from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(30), primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(String(200))
    image: Mapped[str | None] = mapped_column(String(100))
