from typing import Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy.future import select
from app.core import security
from app.core.security import verify_password, get_password_hash

from . import models, schemas

async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    query = select(models.User).where(models.User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: models.User):
    hashed_password = get_password_hash(user_in.password)

    user = models.User(
        email=user_in.email,
        hashed_password=hashed_password
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> models.User | None:
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user