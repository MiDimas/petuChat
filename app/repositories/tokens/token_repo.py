from ..repo.base import BaseRepo
from .token_model import Token
from app.database import async_session_maker
from sqlalchemy import select
from app.repositories import User
from datetime import datetime


class TokenRepo(BaseRepo):
    model = Token

    @classmethod
    async def save_token_by_user_id(cls, user_id: int, token: str, expired: datetime, issued: datetime = datetime.now(),
                                    info: str | None = None, revoked: bool = False):
        async with async_session_maker() as session:
            query = select(User).where(User.id == user_id)
            user = session.scalars(query).one()
            if not user:
                raise ValueError('Пользователь с таким id не найден')
            token_obj = Token(
                refresh_token=token,
                expired_at=expired,
                issued_at=issued,
                client_info=info,
                revoked=revoked
            )
            user.tokens.append(token_obj)
            session.commit()
            return token_obj
