from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

async def create_session(database_url, base) -> AsyncSession:
    engine = create_async_engine(database_url, echo=True, future=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)
    return async_session()
