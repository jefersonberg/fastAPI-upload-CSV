from fastapi import FastAPI
from app.api.v1.endpoints import debt_search, csv_upload, email 
from app.db.mongodb import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def read_main():
    return {"message": "Welcome to Kanastra API"}

app.include_router(csv_upload.router, prefix="/api/v1", tags=["csv_upload"])
app.include_router(email.router, prefix="/api/v1", tags=["send_email"])
app.include_router(debt_search.router, prefix="/api/v1", tags=["debt_search"])
