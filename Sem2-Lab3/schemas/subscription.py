from pydantic import BaseModel

class SubscriptionSchema(BaseModel):
    user_id: int
    currency_id: int
