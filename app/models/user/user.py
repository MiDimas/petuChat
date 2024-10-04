"""
Файлы моделей, содержат основную бизнес-логику для различных сущностей, в данных файлах объединяется
получение данных из репозиториев, дополнительная валидация входных данных, их преобразование и т.д.
"""

from app.repositories.users import UserRepo
from .user_get import UsersGetAll
from .user_post import UserCreateData
from passlib.context import CryptContext


class User:
    @classmethod
    async def get_all_users(cls, params: UsersGetAll):
        return await UserRepo.find_all(**params.to_dict())

    @classmethod
    async def get_user_by_id(cls, user_id: int):
        return await UserRepo.find_one_or_none_by_id(user_id)

    @classmethod
    async def get_full_user_by_id(cls, user_id: int):
        return await UserRepo.find_full_data(user_id)

    @classmethod
    async def create_user(cls, params: UserCreateData):
        if params.password == params.name:
            raise ValueError('Пароль и логин не должны совпадать')
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        try:
            login = params.name.lower().strip()
            password = pwd_context.hash(params.password)
            return await UserRepo.insert_user(**{'name': login, 'password': password})
        except Exception as e:
            raise e
