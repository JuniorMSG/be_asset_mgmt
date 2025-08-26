# 모든 라우터를 가져와서 내보내는 초기화 파일
from fastapi import APIRouter
from app.routers.users import router as users_router
from app.routers.tax import router as tax_router

# 메인 라우터 생성
router = APIRouter()

# 각 모듈의 라우터를 메인 라우터에 포함
router.include_router(users_router)
router.include_router(tax_router)

# 이 모듈에서 router를 import하면 모든 라우터가 포함된 통합 라우터를 가져갈 수 있음