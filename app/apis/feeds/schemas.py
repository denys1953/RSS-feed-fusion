from pydantic import BaseModel, HttpUrl
from datetime import datetime

class SubscriptionCreate(BaseModel):
    url: HttpUrl
class FeedRead(BaseModel):
    id: int
    url: HttpUrl
    title: str
    last_fetched_at: datetime | None = None

    class config:
        from_attributes = True

