from ..repo.base import BaseRepo
from .user_model import User
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from app.database import async_session_maker
from sqlalchemy.future import select


class UserRepo(BaseRepo):
    model = User

    @classmethod
    async def insert_user(cls, **values):
        try:
            return await cls.add(**values)
        except IntegrityError as e:
            raise ValueError('Пользователь с таким логином уже существует')

    @classmethod
    async def find_full_data(cls, user_id: int):
        async with async_session_maker() as session:
            query_user = select(cls.model).options(joinedload(cls.model.emails)).filter_by(id=user_id)
            result = await session.execute(query_user)
            unique_user = result.unique()
            user = unique_user.scalar_one_or_none()

            if not user:
                return None

            return user
