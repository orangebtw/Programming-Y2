from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.subscription import Subscription
from schemas.subscription import SubscriptionSchema
from database import get_db_session

router = APIRouter()

@router.post("/")
async def subscribe_user_to_currency(schema: SubscriptionSchema, session: AsyncSession = Depends(get_db_session)):
    session.add(Subscription(user_id=schema.user_id, currency_id=schema.currency_id))
    try:
        await session.commit()
        return "success"
    except IntegrityError:
        raise HTTPException(status.HTTP_200_OK, "This user has already subscribed to this currency")

@router.delete("/")
async def unsubscribe_user_from_currency(schema: SubscriptionSchema, session: AsyncSession = Depends(get_db_session)):
    await session.execute(delete(Subscription).where(Subscription.user_id == schema.user_id and Subscription.currency_id == schema.currency_id))
    await session.commit()
    return "success"

