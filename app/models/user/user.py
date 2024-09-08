"""
Файлы моделей, содержат основную бизнес-логику для различных сущностей, в данных файлах объединяется
получение данных из репозиториев, дополнительная валидация входных данных, их преобразование и т.д.
"""

from app.repositories.users import UserRepo
from .user_get import UsersGetAll


class User:
    @classmethod
    async def get_all_users(cls, params: UsersGetAll):
        return await UserRepo.find_all(**{
            'id': params.user_id,
            'name': params.name
            })



