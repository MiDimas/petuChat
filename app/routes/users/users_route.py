from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.repositories.users import UserResponseSchema, UserFullResponseSchema
from app.models.user import User, UsersGetAll, UserCreateData, UserLoginData

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/", summary="Получение всех пользователей")
async def get_all_users(query: UsersGetAll = Depends()) -> list[UserResponseSchema]:
    return await User.get_all_users(query)


@router.post("/registration", summary="Создание пользователя")
async def create_new_user(user_data: UserCreateData, response: Response):
    try:
        user_with_tokens = await User.create_user(user_data)
        
        # Устанавливаем refresh токен в httpOnly куки
        response.set_cookie(
            key="refresh_token",
            value=user_with_tokens.tokens["refresh"].token,
            httponly=True,
            # secure=True,  # Для HTTPS
            samesite="lax",
            max_age=30 * 24 * 60 * 60  # 30 дней в секундах
        )
        
        # Возвращаем только пользователя и access токен
        return {
            "user": user_with_tokens.user,
            "access_token": user_with_tokens.tokens["access"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)

@router.post("/login", summary="Авторизация пользователя")
async def login_user(user_data: UserLoginData, response: Response):
    try:
        user_with_tokens = await User.login_user(user_data)
        if not user_with_tokens:
            raise HTTPException(status_code=401, detail='Неверный логин или пароль')
        response.set_cookie(
            key="refresh_token",
            value=user_with_tokens.tokens["refresh"].token,
            httponly=True,
            # secure=True,  # Для HTTPS
            samesite="lax",
            max_age=30 * 24 * 60 * 60  # 30 дней в секундах
        )
        return {
            "user": user_with_tokens.user,
            "access_token": user_with_tokens.tokens["access"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)


@router.post("/logout", summary="Выход из системы")
async def logout_user(response: Response, refresh_token: str = None, request: Request = None):
    try: 
        if not refresh_token:
            refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail='Вы не авторизованы')
        res = await User.logout_user(refresh_token)
        response.delete_cookie("refresh_token")
        if not res:
            raise HTTPException(status_code=400, detail='Возникла ошибка при выходе из системы, токен удален из куки')
        return {"message": "Вы успешно вышли из системы"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except HTTPException as e:
        raise e


@router.get("/token", summary="Поиск по рефреш токену")
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