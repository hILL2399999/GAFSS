from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PaymentRequest(BaseModel):
    user_id: int
    amount: float

@router.post("/")
async def create_payment(payment: PaymentRequest):
    return {"status": "success", "payment": payment.dict()}