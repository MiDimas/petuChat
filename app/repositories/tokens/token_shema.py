from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    refresh_token: str
    expires_at: datetime
    issued_at: datetime
    client_info: str
    revoked: bool
    created_at: datetime
    updated_at: datetime
