from datetime import timedelta, datetime, timezone
from typing import Annotated
from dotenv import load_dotenv

import jwt
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.routes import router_users

load_dotenv()

SECRET_KEY = "97478c86f475f5ed6024098b2488ce03f832d5f5b62b60864dd5847fabd92ba2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "fullname": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$Lg8deIUktDEEGsp76T53gOitA7cXUxYsnqWHqWJa37uFoFsqpdbBK",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     username: str | None = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# class Password(BaseModel):
#     password: str


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#
# def get_password_hash(password: str):
#     return pwd_context.hash(password)
#
#
# # class User(BaseModel):
# #     id: int
# #     name: str
# #     date_create: str
# #     date_update: str
#
#
# def verify_password(plain_password: str, hashed_password: str):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid authentication credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get('sub')
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if not user:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(
#         current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @app.post("/token")
# async def login_for_access_token(
#         form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> Token:
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")
#
#
# @app.get("/user/me", response_model=User)
# async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_user
#
#
# @app.get("/user/me/items/")
# async def read_own_items(
#         current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"items_id": "Foo", "owner": current_user.username}]
#
#
# @app.post("/hash")
# async def get_hash(body: Password):
#     if not body.password:
#         raise HTTPException(
#             status_code=status.HTTP_204_NO_CONTENT,
#             detail="Empty request body",
#         )
#     return get_password_hash(body.password)


app.include_router(router_users)
