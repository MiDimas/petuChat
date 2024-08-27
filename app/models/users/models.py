from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300), unique=True)
    password: Mapped[str] = mapped_column(String(300))
    email: Mapped[str] = mapped_column(String(400))
