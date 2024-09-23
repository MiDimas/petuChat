from pydantic import BaseModel, Field


class UserCreateData(BaseModel):
    name: str = Field(min_length=3)
    password: str = Field(min_length=3)
