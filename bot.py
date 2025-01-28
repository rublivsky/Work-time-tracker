import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.database.models import async_main
# from app.handlers import router
from app.user import user_router

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

async def main():
    await async_main()
    bot = Bot(token=os.getenv("API_KEY"))
    dp = Dispatcher()
    dp.include_routers(
        # router, 
        user_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
