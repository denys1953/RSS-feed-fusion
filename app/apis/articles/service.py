from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.apis.users import models as users_model
from app.apis.feeds.service import get_user_feeds
from app.pagination import PaginationParams

from . import models, schemas

async def get_all_articles(db: AsyncSession) -> List[schemas.ParsedArticle]:
    query = select(models.Article)
    result = await db.execute(query)
    return result.scalars().all()

async def get_user_articles(db: AsyncSession, user: users_model.User, pagination: PaginationParams):
    feeds = await get_user_feeds(db=db, user=user)
    res = []

    # for feed in feeds:
    #     query = select(models.Article).where(models.Article.feed_id == feed)
    #     result = await db.execute(query)
    #     res.append(result.scalars().all())

    query = select(models.Article).where(models.Article.feed_id.in_(feeds)).offset(pagination["skip"]).limit(pagination["limit"])
    result = await db.execute(query)
    res = result.scalars().all()
    
    return res