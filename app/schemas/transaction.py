from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TransactionStatus(str, Enum):
    PENDING = "Ожидание"
    COMPLETED = 'Завершено'
    CANCELLED = 'Отменено'


class TransactionBase(BaseModel):
    amount: float
    recipient_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionDB(TransactionBase):
    id: int
    sender_id: int
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str

    class Config:
        orm_mode = True  # Позволяет использовать ORM-объекты


class TransactionFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[TransactionStatus]
