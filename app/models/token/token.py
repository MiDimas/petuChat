import jwt
from datetime import timedelta, datetime, timezone
from app.config import settings
from .types import TokenData
from app.repositories.tokens import TokenRepo


class Token:
    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None, secret: str = '') -> TokenData:
        to_encode = data.copy()
        issued = datetime.now(timezone.utc)
        if expires_delta:
            expire = issued + expires_delta
        else:
            expire = issued + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret, algorithm='HS256')
        return TokenData(
            token=encoded_jwt,
            expired=expire,
            issued=issued
        )

    @classmethod
    def generate_tokens(cls, data: dict) -> dict[str, TokenData]:
        access_token = cls.create_access_token(data, expires_delta=timedelta(minutes=30), secret=settings.SECRET_KEY)
        refresh_token = cls.create_access_token(data, expires_delta=timedelta(days=30),
                                                secret=settings.SECRET_REFRESH_KEY)
        return {'access': access_token,
                'refresh': refresh_token}

    @classmethod
    async def save_token_for_user(cls, token: TokenData, user_id: int):
        return await TokenRepo.save_token_by_user_id(
            user_id=user_id,
            token=token.token,
            expired=token.expired,
            issued=token.issued
        )

    @classmethod
    def decode_refresh_token(cls, token: str):
        return jwt.decode(token, key=settings.SECRET_REFRESH_KEY, algorithms=['HS256'])

    @classmethod
    async def find_token(cls, token: str, user_id: int):
        return await TokenRepo.find_token_obj(token, user_id)
    
    @classmethod
    async def delete_token(cls, token: str, user_id: int):
        return await TokenRepo.delete_token_by_user_id(token, user_id)