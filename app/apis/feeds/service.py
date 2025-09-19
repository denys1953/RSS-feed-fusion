from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
import feedparser

from app.apis.users import models as user_models
from app.apis.users.models import subscription_table
from . import models, schemas

def get_hostname(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

async def get_feed_by_url(db: AsyncSession, url: str) -> models.Feed | None:
    query = select(models.Feed).where(models.Feed.url == url)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def subscribe_to_feed(db: AsyncSession, feed: schemas.SubscriptionCreate, user: user_models.User):
    url = str(feed.url)
    title = get_hostname(url)

    db_feed = await get_feed_by_url(db, url)

    if not db_feed:
        db_feed = models.Feed(url=url, title=title)
        db.add(db_feed)
        try:
            await db.flush()
        except IntegrityError:
            await db.rollback()
            db_feed = await get_feed_by_url(db, url)
            if not db_feed:
                raise

    stmt = select(subscription_table.c.user_id).where(
        subscription_table.c.user_id == user.id,
        subscription_table.c.feed_id == db_feed.id,
    )
    result = await db.execute(stmt)
    already = result.scalar_one_or_none()
    if not already:
        try:
            await db.execute(
                insert(subscription_table).values(user_id=user.id, feed_id=db_feed.id)
            )
        except IntegrityError:
            await db.rollback()

    await db.commit()
    await db.refresh(db_feed)
    
    return db_feed