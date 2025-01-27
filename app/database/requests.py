from sqlalchemy import select, update, insert
from app.database.models import Base, engine, async_session, UsersORM, WorkTimesORM

def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper

@connection
async def set_user(session, telegram_id, username):
    user = await session.scalar(select(UsersORM).where(UsersORM.telegram_id == telegram_id))

    if not user:
        session.add(UsersORM(telegram_id=telegram_id, username=username))
        await session.commit()
        return False
    else:
        return user

@connection
async def update_user(session, telegram_id, contact):
    await session.execute(update(UsersORM).where(UsersORM.telegram_id == telegram_id).values(contact=contact))
    await session.commit()

@connection
async def get_user(session, telegram_id):
    async with session() as conn:
        return await conn.execute(select(UsersORM).where(UsersORM.telegram_id == telegram_id))
    
@connection
async def set_start_time(session, telegram_id, date, time):
    # Проверяем, есть ли запись для данного пользователя
    record = await session.scalar(select(WorkTimesORM.start_time).where(WorkTimesORM.telegram_id == telegram_id))
    if not record:
        # Создаём новую запись
        session.add(WorkTimesORM(telegram_id=telegram_id, date=date, start_time=time, status=1))
        await session.commit()
        return True
    else:
        # Если запись уже существует, ничего не делаем
        return False


@connection
async def set_end_time(session, telegram_id):
    end_time = await session.scalar(select(WorkTimesORM).where(WorkTimesORM.telegram_id == telegram_id))
    if not end_time:
        await session.execute(update(WorkTimesORM.end_time).where(WorkTimesORM.telegram_id == telegram_id))
        await session.commit()
        return True
    else:
        return False
   
