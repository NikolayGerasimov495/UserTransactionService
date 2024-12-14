import logging

from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

logger = logging.getLogger(__name__)

router = APIRouter()

logger.info("Подключение маршрута аутентификации с использованием JWT.")
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

logger.info("Подключение маршрута регистрации пользователей.")
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]

logger.info("Подключение маршрута пользователей.")
router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)
