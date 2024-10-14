from pydantic import BaseModel
from datetime import datetime


class TokenData(BaseModel):
    token: str
    expired: datetime
    issued: datetime
