"""
В данных файлах содержатся классы для описания схем входных параметров для определенных моделей
"""
from pydantic import BaseModel


class UsersGetAll(BaseModel):
    user_id: int | None = None
    name: str | None = None

    def to_dict(self) -> dict:
        data = {'id': self.user_id, 'name': self.name}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
