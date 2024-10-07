from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.types import str_null_true
from datetime import datetime
from typing import TYPE_CHECKING


class Token(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    refresh_token: Mapped[str] = mapped_column(String(512))
    expires_at: Mapped[datetime]
    issued_at: Mapped[datetime]
    client_info: Mapped[str_null_true]
    revoked: Mapped[bool]

    user: Mapped["User"] = relationship(back_populates="tokens")


if TYPE_CHECKING:
    from .. import User
