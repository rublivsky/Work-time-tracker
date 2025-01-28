import os
import dotenv
from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "").replace("postgres://", "postgresql+asyncpg://")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class UsersORM(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, nullable=True, unique=True)
    username: Mapped[str] = mapped_column(String(length=30), nullable=True)
    contact: Mapped[str] = mapped_column(String(length=20), nullable=True)

class WorkTimesORM(Base):
    __tablename__ = "work_time"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, ForeignKey(UsersORM.telegram_id))
    session_date: Mapped[str] = mapped_column(String(length=20))
    start_time: Mapped[str] = mapped_column(String(length=20), nullable=True)
    end_time: Mapped[str] = mapped_column(String(length=20), nullable=True)
    bonuses: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[Boolean] = mapped_column(Boolean, nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)