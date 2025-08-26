from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/tax",
    tags=["tax"],
    responses={404: {"description": "Not found"}},
)

class TaxRateRequest(BaseModel):
    amount: float
    tax_rate: Optional[float] = 10.0  # 기본 세율 10%
    country_code: Optional[str] = "KR"  # 기본 국가 코드

class TaxCalculationRequest(BaseModel):
    items: List[Dict[str, float]]  # 각 아이템의 가격과 수량
    tax_rate: Optional[float] = 10.0  # 기본 세율 10%
    country_code: Optional[str] = "KR"  # 기본 국가 코드

class TaxResponse(BaseModel):
    original_amount: float
    tax_amount: float
    total_amount: float
    tax_rate: float
    country_code: str

# 국가별 세율 정보 (예시)
COUNTRY_TAX_RATES = {
    "KR": 10.0,  # 한국 10%
    "US": 7.5,   # 미국 7.5% (예시)
    "JP": 10.0,  # 일본 10%
    "CN": 13.0,  # 중국 13%
    "UK": 20.0,  # 영국 20%
}

@router.post("/calculate", response_model=TaxResponse)
async def calculate_tax(request: TaxRateRequest):
    """
    금액과 세율을 기반으로 세금을 계산합니다.
    세율이 제공되지 않으면 국가 코드에 따른 기본 세율을 사용합니다.
    """
    # 국가 코드에 따른 세율 적용
    tax_rate = request.tax_rate
    if request.country_code in COUNTRY_TAX_RATES and not request.tax_rate:
        tax_rate = COUNTRY_TAX_RATES[request.country_code]
    
    # 세금 계산
    original_amount = request.amount
    tax_amount = original_amount * (tax_rate / 100)
    total_amount = original_amount + tax_amount
    
    return TaxResponse(
        original_amount=original_amount,
        tax_amount=round(tax_amount, 2),
        total_amount=round(total_amount, 2),
        tax_rate=tax_rate,
        country_code=request.country_code
    )

@router.post("/calculate-items", response_model=TaxResponse)
async def calculate_tax_for_items(request: TaxCalculationRequest):
    """
    여러 아이템의 가격과 수량을 기반으로 총 세금을 계산합니다.
    세율이 제공되지 않으면 국가 코드에 따른 기본 세율을 사용합니다.
    """
    # 국가 코드에 따른 세율 적용
    tax_rate = request.tax_rate
    if request.country_code in COUNTRY_TAX_RATES and not request.tax_rate:
        tax_rate = COUNTRY_TAX_RATES[request.country_code]
    
    # 총 금액 계산
    original_amount = sum(item.get("price", 0) * item.get("quantity", 1) for item in request.items)
    tax_amount = original_amount * (tax_rate / 100)
    total_amount = original_amount + tax_amount
    
    return TaxResponse(
        original_amount=original_amount,
        tax_amount=round(tax_amount, 2),
        total_amount=round(total_amount, 2),
        tax_rate=tax_rate,
        country_code=request.country_code
    )

@router.get("/rates", response_model=Dict[str, float])
async def get_tax_rates():
    """
    지원되는 모든 국가의 세율 정보를 반환합니다.
    """
    return COUNTRY_TAX_RATES

@router.get("/rate/{country_code}", response_model=float)
async def get_tax_rate_by_country(country_code: str):
    """
    특정 국가의 세율 정보를 반환합니다.
    """
    if country_code not in COUNTRY_TAX_RATES:
        raise HTTPException(status_code=404, detail=f"Tax rate for country code '{country_code}' not found")
    
    return COUNTRY_TAX_RATES[country_code]