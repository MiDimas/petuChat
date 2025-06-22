import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings


class Auth:
    security = HTTPBearer()

    
    @classmethod
    async def verify_access_token(cls, credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials

        try: 
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Срок действия токена истек')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Неверный токен')
        
        