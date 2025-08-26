from fastapi import FastAPI
from app.routers import router
from app.database.database import engine
from app.models import models

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 태그 설명 정의
tags_metadata = [
    {
        "name": "users",
        "description": "사용자 관리 작업",
    },
    {
        "name": "tax",
        "description": "세금 계산 관련 작업",
    },
    {
        "name": "root",
        "description": "루트 엔드포인트",
    },
    {
        "name": "greeting",
        "description": "인사 관련 엔드포인트",
    },
]

# 태그 그룹 정의 (상단 드롭다운 메뉴용)
openapi_extra = {
    "x-tagGroups": [
        {
            "name": "API 그룹",
            "tags": ["users", "tax"]
        },
        {
            "name": "일반 엔드포인트",
            "tags": ["root", "greeting"]
        }
    ]
}

app = FastAPI(
    title="FastAPI with MySQL",
    description="FastAPI 애플리케이션과 MySQL 연동 예제",
    openapi_tags=tags_metadata,  # 태그 메타데이터 추가
    openapi_extra=openapi_extra  # 태그 그룹 정의 추가
)

# 통합된 라우터 등록
app.include_router(router)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World! Welcome to FastAPI with MySQL"}

@app.get("/hello/{name}", tags=["greeting"])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}