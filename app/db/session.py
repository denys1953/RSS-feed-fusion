from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SyncSession


engine = create_async_engine(
	settings.DATABASE_URL,
	echo=settings.DEBUG,
	pool_size=20,
	max_overflow=30,
	pool_pre_ping=True,
	pool_recycle=3600,
)

SessionLocal = sessionmaker(
	engine, 
	class_=AsyncSession, 
	autocommit=False, 
	autoflush=False,
	expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


sync_db_url = str(settings.DATABASE_URL).replace("+asyncpg", "")

sync_engine = create_engine(
    sync_db_url,
    echo=settings.DEBUG,
    pool_pre_ping=True
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)

def get_sync_db() -> SyncSession:
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()