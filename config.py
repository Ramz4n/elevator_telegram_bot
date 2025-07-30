from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": 3306,
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "db": os.getenv("DB_NAME"),
}
