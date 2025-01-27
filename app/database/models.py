from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

engine = create_async_engine(url='sqlite+aiosqlite:///app/database/db.sqlite3')

async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class UsersORM(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, nullable=True)
    username: Mapped[str] = mapped_column(String(length=30), nullable=True)
    contact: Mapped[str] = mapped_column(String(length=20), nullable=True)

class WorkTimesORM(Base):
    __tablename__ = "work_time"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, ForeignKey(UsersORM.telegram_id))
    date: Mapped[str] = mapped_column(String(length=20))
    start_time: Mapped[str] = mapped_column(String(length=20), nullable=True)
    end_time: Mapped[str] = mapped_column(String(length=20), nullable=True)
    bonuses: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[Boolean] = mapped_column(Boolean, nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)