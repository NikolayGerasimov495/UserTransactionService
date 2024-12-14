import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Transaction, User
from app.validators.validators import (validate_not_self_transaction,
                                       validate_sufficient_balance,
                                       validate_user_exists)

logger = logging.getLogger(__name__)


async def service_create_transaction(transaction_data,
                                     user: User,
                                     session:
                                     AsyncSession):

    await validate_user_exists(transaction_data.recipient_id, session)

    await validate_not_self_transaction(user.id, transaction_data.recipient_id)

    await validate_sufficient_balance(user.balance, transaction_data.amount)

    db_obj = Transaction(
        amount=transaction_data.amount,
        sender_id=user.id,
        recipient_id=transaction_data.recipient_id,
        status="В ожидании"
    )
    session.add(db_obj)
    user.balance -= transaction_data.amount

    recipient = await session.get(User, transaction_data.recipient_id)
    if recipient:
        recipient.balance += transaction_data.amount

    await session.commit()
    await session.refresh(db_obj)

    db_obj.status = "Завершено"
    await session.commit()
    await session.refresh(db_obj)

    logger.info(
        f"Транзакция создана: {db_obj.id}, отправитель: {user.id}, "
        f"получатель: {transaction_data.recipient_id}, "
        f"сумма: {transaction_data.amount}")

    return db_obj
