from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from ..emails import EmailSchema


class  UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., description="Имя пользователя")
    token: str | None = Field(None, description="Токен пользователя")
    created_at: datetime = Field(..., description="Дата регистрации")
    updated_at: datetime = Field(..., description="Дата последнего обновления")


class UserFullResponseSchema(UserResponseSchema):
    password: str = Field(..., description="Хэш пароля")
    emails: list["EmailSchema"] = Field([], description="Почты пользователя")


class UserSchema(UserResponseSchema):
    password: str = Field(..., description="Хэшированный пароль пользователя")


class UserCreateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None
