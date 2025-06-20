from ..repo.base import BaseRepo
from .token_model import Token
from app.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.repositories import User
from datetime import datetime
from passlib.context import CryptContext


class TokenRepo(BaseRepo):
    model = Token

    @classmethod
    async def save_token_by_user_id(cls, user_id: int, token: str, expired: datetime,
                                    issued: datetime = datetime.now(),
                                    info: str | None = None, revoked: bool = False):
        async with async_session_maker() as session:
            query = select(User).where(User.id == user_id).options(selectinload(User.tokens))
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            if not user:
                raise ValueError('Пользователь с таким id не найден')
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
            token_hash = pwd_context.hash(token)
            token_obj = Token(
                refresh_token=token_hash,
                expires_at=expired.replace(tzinfo=None),
                issued_at=issued.replace(tzinfo=None),
                client_info=info,
                revoked=revoked
            )
            user.tokens.append(token_obj)
            await session.commit()
            return token_obj

    @classmethod
    async def find_token_obj(cls, token: str, user_id: int):
        async with async_session_maker() as session:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

            query = select(Token).where(Token.user_id == user_id)
            result = await session.execute(query)
            user_tokens = result.scalars().all()
            for t in user_tokens:
                if pwd_context.verify(token, t.refresh_token):
                    return t
            return None
    
    @classmethod
    async def delete_token_by_user_id(cls, token: str, user_id: int):
        async with async_session_maker() as session:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

            query = select(Token).where(Token.user_id == user_id)
            result = await session.execute(query)
            user_tokens = result.scalars().all()
            for t in user_tokens:
                if pwd_context.verify(token, t.refresh_token):
                    await session.delete(t)
                    await session.commit()
                    return True
            return False
