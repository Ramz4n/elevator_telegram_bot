import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import basic

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация обработчиков
dp.include_router(basic.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
