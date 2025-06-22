from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import mapped_column

from .helpers.utc_now import utc_now

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=utc_now)]
str_uniq = Annotated[str, mapped_column(nullable=False, unique=True)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

