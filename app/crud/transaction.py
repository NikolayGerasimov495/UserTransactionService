from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionFilter


class CRUDTransaction(CRUDBase):
    async def get_filtered_transactions(self,
                                        session: AsyncSession,
                                        user_id: int,
                                        filters: TransactionFilter):
        query = select(Transaction).where(
            or_(Transaction.sender_id == user_id, Transaction.recipient_id == user_id)
        )

        if filters.start_date:
            query = query.where(Transaction.timestamp >= filters.start_date)
        if filters.end_date:
            query = query.where(Transaction.timestamp <= filters.end_date)
        if filters.status:
            query = query.where(Transaction.status == filters.status)

        result = await session.execute(query)
        return result.scalars().all()


transaction_crud = CRUDTransaction(Transaction)
