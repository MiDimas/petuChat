from fastapi import APIRouter, Depends, HTTPException
from app.repositories.users import UserResponseSchema, UserFullResponseSchema
from app.models.user import User, UsersGetAll, UserCreateData

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/", summary="Получение всех пользователей")
async def get_all_users(query: UsersGetAll = Depends()) -> list[UserResponseSchema]:
    return await User.get_all_users(query)


@router.post("/registration", summary="Создание пользователя")
async def create_new_user(user_data: UserCreateData):
    try:
        return await User.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)


@router.get("/token", summary="Поиск по токену")
async def find_refresh_token(token: str):
    try:
        return await User.verify_user_refresh_token(token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)


@router.get("/{id}", summary="Получение пользователя по id")
async def get_user_by_id(user_id: int, full: int | None = 0) -> UserResponseSchema | UserFullResponseSchema:
    if full:
        return await User.get_full_user_by_id(user_id)
    return await User.get_user_by_id(user_id)