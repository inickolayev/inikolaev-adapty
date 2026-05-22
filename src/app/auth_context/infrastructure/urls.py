from fastapi import APIRouter

from app.auth_context.infrastructure.ports import http

router = APIRouter()
router.include_router(http.register_router, prefix='/register')
router.include_router(http.login_router, prefix='/login')
router.include_router(http.refresh_router, prefix='/refresh')
router.include_router(http.confirm_email_router, prefix='/confirm-email')
router.include_router(http.password_reset_request_router, prefix='/password-reset/request')
router.include_router(http.password_reset_confirm_router, prefix='/password-reset/confirm')
router.include_router(http.change_email_router, prefix='/change-email')
router.include_router(http.me_router, prefix='/me')
