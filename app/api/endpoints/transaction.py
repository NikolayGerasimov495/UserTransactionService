import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.transaction import transaction_crud
from app.models import User
from app.schemas.transaction import (TransactionCreate, TransactionDB,
                                     TransactionFilter)
from app.services.transactions import service_create_transaction

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=TransactionDB,
)
async def create_transaction(
        transaction: TransactionCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создает новую транзакцию между пользователями.
    Проверяет наличие получателя и достаточность баланса отправителя.
    """

    new_transaction = await service_create_transaction(
        transaction, user, session)

    logger.info(f"Пользователь {user.id} создал "
                f"транзакцию {new_transaction.id}")
    return new_transaction


@router.get(
    "/",
    response_model=list[TransactionDB]
)
async def get_transactions_with_filters(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        skip: int = 0,
        limit: int = 10,
        filters: TransactionFilter = Depends()
):
    """
    Получает историю транзакций для текущего пользователя
    с пагинацией и фильтрацией.
    """
    logger.info(
        f"Пользователь {user.id} "
        f"запрашивает историю транзакций с фильтрами: {filters},"
        f"пропуск: {skip}, лимит: {limit}")

    transactions = await transaction_crud.get_filtered_transactions(
        session, user.id, filters)

    logger.info(f"Найдено {len(transactions)} транзакций "
                f"для пользователя {user.id}")

    return transactions[skip: skip + limit]
