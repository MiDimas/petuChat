from pydantic import BaseModel, Field, ConfigDict, EmailStr


class EmailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    address: EmailStr = Field(..., description="Email адрес пользователя")
