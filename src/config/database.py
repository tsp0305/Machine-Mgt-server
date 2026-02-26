from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base
from settings import settings

DATABASE_URL = settings.DATABASE_URL

Base = declarative_base()

engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
async def get_db():
    async with SessionLocal() as session:
        yield session
