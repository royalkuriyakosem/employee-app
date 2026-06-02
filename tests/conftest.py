import pytest_asyncio

# Same async-flavoured SQLAlchemy imports as the previous slide.
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = async_sessionmaker(engine, expire_on_commit=False)()

    try:
        yield db

    except Exception:
        print("I am exception")
