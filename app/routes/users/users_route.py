from fastapi import APIRouter
from app.repositories.users import UserSchema, UserRepo

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.get("/", summary="Получение всех пользователей", response_model=list[UserSchema])
async def get_all_users():
    return await UserRepo.find_all()
