"""
Файлы моделей, содержат основную бизнес-логику для различных сущностей, в данных файлах объединяется
получение данных из репозиториев, дополнительная валидация входных данных, их преобразование и т.д.
"""
from pydantic import BaseModel

from app.repositories.users import UserRepo, UserResponseSchema
from .user_get import UsersGetAll
from .user_post import UserCreateData
from passlib.context import CryptContext
from ..token import Token, TokenData
from fastapi import HTTPException


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
            new_user = await UserRepo.insert_user(**{'name': login, 'password': password})
            if new_user:
                id_user = new_user.id
                tokens = Token.generate_tokens({"sub": login, "id": id_user})
                result = await Token.save_token_for_user(tokens["refresh"], id_user)
                if not result:
                    return HTTPException(
                        status_code=400,
                        detail='Возникла ошибка при записи пользователя'
                    )
                return UserCreateWithTokens(
                    user=new_user,
                    tokens=tokens
                )
            raise HTTPException(
                status_code=409,
                detail='Данный пользователь уже существует'
            )
        except Exception as e:
            raise e

    @classmethod
    async def verify_user_refresh_token(cls, token: str):

        info = Token.decode_refresh_token(token)
        current_token = await Token.find_token(token, info['id'])
        return current_token


class UserCreateWithTokens(BaseModel):
    user: UserResponseSchema
    tokens: dict[str, TokenData]
