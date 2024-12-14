from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Transaction(Base):
    amount = Column(Float)
    sender_id = Column(Integer, ForeignKey('user.id'))
    recipient_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String, default="Ожидание")

    sender = relationship("User", foreign_keys=[sender_id],
                          back_populates="sent_transactions")
    recipient = relationship("User", foreign_keys=[recipient_id],
                             back_populates="received_transactions")