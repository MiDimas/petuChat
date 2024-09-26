from fastapi import APIRouter, Depends
from app.repositories.users import UserResponseSchema, UserCreateResponseSchema
from app.models.user import User, UsersGetAll, UserCreateData

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/", summary="Получение всех пользователей")
async def get_all_users(query: UsersGetAll = Depends()):
    return await User.get_all_users(query)


@router.get("/{id}", summary="")
async def get_user_by_id(user_id: int) -> UserResponseSchema:
    return await User.get_user_by_id(user_id)


@router.post("/registration", summary="Создание пользователя", response_model=UserResponseSchema)
async def create_new_user(user_data: UserCreateData):
    return await User.create_user(user_data)
