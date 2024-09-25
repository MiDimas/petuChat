from ..repo.base import BaseRepo
from .user_model import User


class UserRepo(BaseRepo):
    model = User

    @classmethod
    async def insert_user(cls, **values):
        return await cls.add(**values)
