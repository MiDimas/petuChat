from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    id: int
    name: str
    date_create: str
    date_update: str


def fake_decode_token(token):
    return User(
        id=1, name=token+'fakedecoded', date_create='15.08.2024', date_update='15.08.2024'
    )


async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/user/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
