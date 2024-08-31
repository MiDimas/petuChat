from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models import Email
from app.types import str_uniq


class User(Base):
    name: Mapped[str_uniq] = mapped_column(String(300), unique=True)
    password: Mapped[str] = mapped_column(String(300))
    emails: Mapped[list["Email"]] = relationship(back_populates="user", cascade="all, delete-orphan")
