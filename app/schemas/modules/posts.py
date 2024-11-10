from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone


class PostCreate(BaseModel):
    id: Optional[str] = None
    title: str
    author_id: int
    content: str
    create_at: Optional[datetime] = datetime.now(timezone.utc)
    publishe_at: Optional[datetime] = None
    published: Optional[bool] = False

    class Config:
        orm_mode = True

    @classmethod
    def create(cls, **data):
        if not data.get("create_at"):
            data["create_at"] = datetime.now()
        return cls(**data)
