from fastapi import APIRouter, HTTPException, Query
from app.services.debt_service import find_debt

router = APIRouter()

@router.get("/search-debt/")
async def search_debt(
    governmentId: str = Query(None),
    email: str = Query(None),
    debtId: str = Query(None)
):
    try:
        results = find_debt(governmentId, email, debtId)
        if not results:
            raise HTTPException(status_code=404, detail="No debt records found.")
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
