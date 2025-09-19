from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.db.session import get_db
from app.core.security import get_current_user
from . import schemas, service, models

router = APIRouter(
	# dependencies=[Depends(get_current_user)]
)

@router.post("/register", response_model=schemas.UserRead)
async def create_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing_user = await service.get_user_by_email(db=db, email=user_in.email)

    if existing_user:
        raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User with this email already exists"
		)

    user = await service.create_user(db=db, user_in=user_in)
    return user


