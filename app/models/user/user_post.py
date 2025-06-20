import re

from pydantic import BaseModel, Field, field_validator


class UserCreateData(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=3, max_length=256)

    @field_validator("name")
    @classmethod
    def validate_name(cls, values: str) -> str:
        values = values.strip()
        if len(values) < 3 or len(values) > 30:
            raise ValueError('Логин не может содержать меньше 3 и больше 30 символов')
        if not re.match(r'^[A-Za-z0-9._-]*$', values):
            raise ValueError('Логин может содержать только латинские буквы, цифры и символы ".-_"')
        if not re.match(r'(?=.*[a-zA-Z])', values):
            raise ValueError('Логин не может состоять только из цифр или спец-символов')
        reserved_names = ['root', 'admin', 'support']
        if values.lower() in reserved_names:
            raise ValueError('Логин не может использовать зарезервированное имя')
        return values

    @field_validator("password")
    @classmethod
    def validate_password(cls, values: str) -> str:
        if not re.match(r'(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}', values):
            raise ValueError('Пароль должен содержать как минимум одну заглавную,' +
                             ' одну прописную буквы латинского алфавита, а так же одну цифру' +
                             ' и содержать не менее 8 символов')
        return values
    
class UserLoginData(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=3, max_length=256)
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, values: str) -> str:
        values = values.strip()
        if not values:
            raise ValueError("Логин не может быть пустым")
        if len(values) < 3 or len(values) > 30:
            raise ValueError("Логин не может содержать меньше 3 и больше 30 символов")
        return values
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, values: str) -> str:
        if not values:
            raise ValueError("Пароль не может быть пустым")
        return values
