from fastapi import APIRouter, Depends
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.subscription import Subscription
from schemas.subscription import SubscriptionSchema
from schemas.response import ResponseSchema, ErrorSchema
from database import get_db_session

router = APIRouter()

@router.post("/")
async def subscribe_user_to_currency(schema: SubscriptionSchema, session: AsyncSession = Depends(get_db_session)):
    session.add(Subscription(user_id=schema.user_id, currency_id=schema.currency_id))
    await session.commit()
    return ResponseSchema(success=True, error=ErrorSchema(message="User subscribed successfully"))

@router.delete("/")
async def unsubscribe_user_from_currency(schema: SubscriptionSchema, session: AsyncSession = Depends(get_db_session)):
    await session.execute(delete(Subscription).where(Subscription.user_id == schema.user_id and Subscription.currency_id == schema.currency_id))
    await session.commit()
    return ResponseSchema(success=True, error=ErrorSchema(message="User unsubscribed successfully"))

