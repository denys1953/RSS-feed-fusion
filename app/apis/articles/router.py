from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.db.session import get_db
from app.core.security import get_current_user
from app.core import feed_parser
from app.pagination import PaginationParams, get_pagination_params 
from . import schemas, service, models
from app.apis.users import models as users_model

router = APIRouter(
	# dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[schemas.ParsedArticle])
async def get_user_articles(
	db: AsyncSession = Depends(get_db),
	current_user: users_model.User = Depends(get_current_user),
	pagination: PaginationParams = Depends(get_pagination_params)
):
	articles = await service.get_user_articles(db=db, user=current_user, pagination=pagination)
	return articles