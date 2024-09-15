from fastapi import APIRouter
from app.repositories.users import UserSchema
from app.models.user import User, UsersGetAll

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/{user_id}", summary="Получение всех пользователей", response_model=list[UserSchema])
async def get_all_users(user_id: int | None):
    user = UsersGetAll(user_id=user_id, name=None)
    return await User.get_all_users(user)
