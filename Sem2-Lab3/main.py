from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from models.base import Base
from models.currency import Currency
from database import engine, AsyncSessionLocal
from utils import fetch_currencies

from routers import currencies
from routers import users
from routers import subscriptions

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(lambda conn: Currency.__table__.drop(conn, checkfirst=True))
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        currencies = await asyncio.to_thread(fetch_currencies)
        session.add_all(map(
            lambda c: Currency(code=c["CharCode"], name=c["Name"]),
            currencies
        ))
        await session.commit()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(currencies.router, prefix="/currencies")
app.include_router(users.router, prefix="/users")
app.include_router(subscriptions.router, prefix="/subscriptions")

