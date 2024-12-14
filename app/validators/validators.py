import logging
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

logger = logging.getLogger(__name__)


async def validate_user_exists(user_id: int, session: AsyncSession):
    user = await session.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()
    if not user:
        logger.warning(f"Пользователь с ID {user_id} не найден.")
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Пользователь не найден")


async def validate_sufficient_balance(balance: float, amount: float):
    if balance < amount:
        logger.warning(f"Недостаточно средств: {balance}, попытка снять: {amount}.")
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Не хватает денежных средств")


async def validate_not_self_transaction(sender_id: int, recipient_id: int):
    if sender_id == recipient_id:
        logger.warning(f"Попытка перевода от {sender_id} самому себе {recipient_id}.")
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя отправить средства самому себе"
        )
