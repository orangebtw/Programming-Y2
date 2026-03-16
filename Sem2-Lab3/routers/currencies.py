from fastapi import APIRouter, Depends
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session
from schemas.currency import CurrencySchema
from models.currency import Currency
from database import engine
from utils import fetch_currencies

router = APIRouter()


@router.get("/")
async def currencies(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Currency))
    currencies = result.scalars().all()
    data = list(map(lambda c: CurrencySchema.model_validate(c), currencies))
    return data

@router.post("/update")
async def update_currencies(session: AsyncSession = Depends(get_db_session)):
    async with engine.begin() as conn:
        await conn.run_sync(Currency.__table__.drop)
        await conn.run_sync(Currency.__table__.create)

    currencies = await asyncio.to_thread(fetch_currencies)
    session.add_all(map(
        lambda c: Currency(code=c["CharCode"], name=c["Name"]),
        currencies
    ))
    await session.commit()
    return "success"
