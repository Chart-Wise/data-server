from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class UpbitTickerDTO(BaseModel):
    user_id: str = Field(..., description="토큰에서 추출한 사용자 ID") # 추가
    code: str = Field(..., alias="code")
    trade_price: Decimal = Field(..., alias="tp")
    trade_timestamp: int = Field(..., alias="ttms")
    ask_bid: str = Field(..., alias="ab")

    model_config = ConfigDict(populate_by_name=True)