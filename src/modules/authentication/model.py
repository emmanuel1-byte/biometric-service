from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime, timezone


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
    )
    fullname: str = Field(nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    public_key: str = Field(unique=True, index=True, nullable=True)
    password: str = Field(nullable=True)
    verified: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
