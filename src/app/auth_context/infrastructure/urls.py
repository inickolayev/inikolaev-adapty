from fastapi import APIRouter

from app.auth_context.infrastructure.ports import http

router = APIRouter()
router.include_router(http.register_router, prefix='/register')
router.include_router(http.login_router, prefix='/login')
router.include_router(http.refresh_router, prefix='/refresh')
router.include_router(http.me_router, prefix='/me')
