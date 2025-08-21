import asyncio
import threading
import sys
import os
import subprocess
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import basic
import pystray
from PIL import Image, ImageDraw

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(basic.router)

# === ЛОГИ В ФАЙЛ ===
LOG_FILE = "bot.log"
sys.stdout = open(LOG_FILE, "w", encoding="utf-8")
sys.stderr = sys.stdout

# === Функция иконки ===
def create_image():
    # 16x16 иконка (простая красная точка)
    image = Image.new("RGB", (64, 64), color=(0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill=(255, 0, 0))
    return image

def on_logging(icon, item):
    # Открываем лог в блокноте
    subprocess.Popen(["notepad.exe", LOG_FILE])

def on_exit(icon, item):
    icon.stop()
    os._exit(0)

# === Айограм в отдельном потоке ===
async def main():
    await dp.start_polling(bot)

def run_aiogram():
    asyncio.run(main())

# === Запуск трей-иконки ===
def setup_tray():
    icon = pystray.Icon(
        "bot",
        create_image(),
        "Telegram Bot",
        menu=pystray.Menu(
            pystray.MenuItem("Logging", on_logging),
            pystray.MenuItem("Exit", on_exit)
        )
    )
    icon.run()

if __name__ == "__main__":
    # Бот в отдельном потоке
    threading.Thread(target=run_aiogram, daemon=True).start()
    # Трэй-меню
    setup_tray()
