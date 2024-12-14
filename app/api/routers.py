from fastapi import APIRouter

from app.api.endpoints import transaction_router, user_router

main_router = APIRouter()
main_router.include_router(
    transaction_router, prefix='/transaction', tags=['Transaction']
)
main_router.include_router(user_router)
