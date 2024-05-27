from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_service import process_csv
from typing import Optional

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Invalid file type.")
        
        await process_csv(file)
        return {"message": "File processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
