import jwt
from datetime import timedelta, datetime, timezone
from app.config import settings


class Token:
    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None, secret: str = '') -> dict:
        to_encode = data.copy()
        issued = datetime.now(timezone.utc)
        if expires_delta:
            expire = issued + expires_delta
        else:
            expire = issued + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret, algorithm='HS256')
        return {
            "token": encoded_jwt,
            "expired": expire,
            "issued": issued
        }

    @classmethod
    def generate_tokens(cls, data: dict) -> dict:
        access_token = cls.create_access_token(data, expires_delta=timedelta(minutes=30), secret=settings.SECRET_KEY)
        refresh_token = cls.create_access_token(data, expires_delta=timedelta(days=30),
                                                secret=settings.SECRET_REFRESH_KEY)
        return {'access': access_token,
                'refresh': refresh_token}

    @classmethod
    async def save_token_for_user(cls, token):
        pass
