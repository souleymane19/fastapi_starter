from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    name: str
    email: str
    hashed_password: str
    is_active: bool = False
    validation_code : Optional[str] = Field(None)
    validation_code_expires_at :Optional[datetime] = Field(None)
