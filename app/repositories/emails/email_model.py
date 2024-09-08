from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.types import str_uniq
from typing import TYPE_CHECKING


class Email(Base):
    address: Mapped[str_uniq]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship(back_populates='emails')


if TYPE_CHECKING:
    from .. import User
