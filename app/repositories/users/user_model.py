from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.types import str_uniq, str_null_true
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Email


class User(Base):
    name: Mapped[str_uniq] = mapped_column(String(300), unique=True)
    password: Mapped[str] = mapped_column(String(300))
    token: Mapped[str_null_true] = mapped_column(String(400))
    emails: Mapped[list["Email"]] = relationship(back_populates="user", cascade="all, delete-orphan")
