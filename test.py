# import asyncio
# from app.database.requests import get_status
# from app.database.models import async_session
from app.user import user_router, local_time

# def connection(func):
#     async def wrapper(*args, **kwargs):
#         async with async_session() as session:
#             return await func(session, *args, **kwargs)
#     return wrapper

# @connection
# async def main(session):
#     status = await get_status('536212014')
#     print(status)


# print(local_time('01-01 00:00', 'Europe/Kyiv'))
