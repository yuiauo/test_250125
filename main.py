from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import Login
from services import get_db


app = FastAPI()


@app.post("/login")
async def login(log_data: Login, db: AsyncSession = Depends(get_db)):
    ...


@app.get("/patients")
async def patients(user_id: int, db: AsyncSession = Depends(get_db)):
    ...
