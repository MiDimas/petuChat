"""
В данных файлах содержатся классы для описания схем входных параметров для определенных моделей
"""
from pydantic import BaseModel


class UsersGetAll(BaseModel):
    user_id: int | None = None,
    name: str | None = None
