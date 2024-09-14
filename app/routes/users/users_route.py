from fastapi import APIRouter
from app.repositories.users import UserSchema
from app.models.user import User, UsersGetAll

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/{user_id}", summary="Получение всех пользователей", response_model=list[UserSchema])
async def get_all_users(user_id: int):
    return await User.get_all_users(request_body)
