from fastapi import APIRouter, Depends
from app.repositories.users import UserResponseSchema, UserCreateResponseSchema, UserFullResponseSchema
from app.models.user import User, UsersGetAll, UserCreateData

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/", summary="Получение всех пользователей")
async def get_all_users(query: UsersGetAll = Depends()) -> list[UserResponseSchema]:
    return await User.get_all_users(query)


@router.get("/{id}", summary="Получение пользователя по id")
async def get_user_by_id(user_id: int, full: int | None = 0) -> UserResponseSchema | UserFullResponseSchema:
    if full:
        return await User.get_full_user_by_id(user_id)
    return await User.get_user_by_id(user_id)


@router.post("/registration", summary="Создание пользователя")
async def create_new_user(user_data: UserCreateData) -> UserResponseSchema:
    return await User.create_user(user_data)
