from fastapi import APIRouter, HTTPException, Body
from app.services.email_service import send_email

router = APIRouter()

@router.post("/send-email")
async def send_email_endpoint(governmentId: str = Body(...), email: str = Body(...), debtId: str = Body(...)):
    try:
        send_email(governmentId, email, debtId)
        return {"message": "Email sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))