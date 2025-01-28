import asyncio
from app.database.requests import get_status
from app.database.models import async_session

def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper

@connection
async def main(session):
    status = await get_status('536212014')
    print(status)

if __name__ == "__main__":
    asyncio.run(main())