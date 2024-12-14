from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Float
from sqlalchemy.orm import relationship

from app.core.db import Base

from .transaction import Transaction


class User(SQLAlchemyBaseUserTable[int], Base):
    balance = Column(Float, default=100)

    sent_transactions = relationship("Transaction",
                                     foreign_keys=[Transaction.sender_id],
                                     back_populates="sender")
    received_transactions = relationship("Transaction",
                                         foreign_keys=[Transaction.recipient_id],
                                         back_populates="recipient")
