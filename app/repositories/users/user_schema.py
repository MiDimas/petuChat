from typing import TYPE_CHECKING
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from ..emails import EmailSchema


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    password: str = Field(..., description="Хэшированный пароль пользователя")
    token: str = Field(None, description="Токен пользователя")
    emails: list["EmailSchema"] = Field(None, description="Почты пользователя")
    created_at: datetime = Field(..., description="Дата регистрации")
    updated_at: datetime = Field(..., description="Дата последнего обновления")
