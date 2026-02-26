from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base
from settings import settings

DATABASE_URL = settings.DATABASE_URL

# DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_VFKP92SqtrpB@ep-winter-sunset-a18ex91w-pooler.ap-southeast-1.aws.neon.tech/neondb"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
async def get_db():
    async with SessionLocal() as session:
        yield session
