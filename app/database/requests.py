from sqlalchemy import select, update, insert, text
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
async def get_status(session, telegram_id):
    # Check if there is an ongoing session (status is True)
    record = await session.scalar(
        select(WorkTimesORM.status)
        .where(
            WorkTimesORM.telegram_id == telegram_id,
            WorkTimesORM.status == True
        )
    )
    return bool(record)

@connection
async def set_start_time(session, telegram_id, date, time):
    # Check if there is an ongoing session for the user
    ongoing_session = await session.scalar(
        select(WorkTimesORM)
        .where(
            WorkTimesORM.telegram_id == telegram_id,
            WorkTimesORM.status == True
        )
    )
    if not ongoing_session:
        # Create a new session record
        session.add(WorkTimesORM(telegram_id=telegram_id, session_date=date, start_time=time, status=True))
        await session.commit()
        return True
    else:
        # If there is an ongoing session, do nothing
        return False

@connection
async def set_end_time(session, telegram_id, date, time):
    # Check if there is an ongoing session for the user
    ongoing_session = await session.scalar(
        select(WorkTimesORM)
        .where(
            WorkTimesORM.telegram_id == telegram_id,
            WorkTimesORM.status == True
        )
    )
    if ongoing_session:
        # Update the end time and status of the ongoing session
        await session.execute(
            update(WorkTimesORM)
            .where(
                WorkTimesORM.telegram_id == telegram_id,
                WorkTimesORM.status == True
            )
            .values(end_time=time, status=False)
        )
        await session.commit()
        return True
    else:
        # If there is no ongoing session, return False
        return False
