from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.types import str_uniq
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Email
    from .. import Token


class User(Base):
    name: Mapped[str_uniq] = mapped_column(String(300), unique=True)
    password: Mapped[str] = mapped_column(String(300))
    tokens: Mapped[list["Token"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    emails: Mapped[list["Email"]] = relationship(back_populates="user", cascade="all, delete-orphan")
