from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.db.session import get_db
from app.core.security import get_current_user
from . import schemas, service, models
from app.apis.users import models as users_model

router = APIRouter(
	# dependencies=[Depends(get_current_user)]
)

@router.post("/subscribe", response_model=schemas.FeedRead)
async def subscribe_to_feed(
    feed_in: schemas.SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: users_model.User = Depends(get_current_user) 
):
    feed = await service.subscribe_to_feed(db=db, feed=feed_in, user=current_user)
    return feed