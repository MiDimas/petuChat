"""
Файлы моделей, содержат основную бизнес-логику для различных сущностей, в данных файлах объединяется
получение данных из репозиториев, дополнительная валидация входных данных, их преобразование и т.д.
"""

from app.repositories.users import UserRepo
from .user_get import UsersGetAll
from .user_post import UserCreateData


class User:
    @classmethod
    async def get_all_users(cls, params: UsersGetAll):
        return await UserRepo.find_all(**{
            'id': params.user_id,
            'name': params.name
            })

    @classmethod
    async def get_user_by_id(cls, user_id: int):
        return await UserRepo.find_one_or_none_by_id(user_id)


    @classmethod
    async def create_user(cls, params: UserCreateData):
        return await UserRepo.insert_user(**{'name': params.name, 'password': params.password})

