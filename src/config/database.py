from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/machine"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
async def get_db():
    async with SessionLocal() as session:
        yield session
