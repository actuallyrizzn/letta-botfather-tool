import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE')
API_BEARER_TOKEN = os.getenv('API_BEARER_TOKEN')
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 57431))

if not all([TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE]):
    raise RuntimeError('Missing required Telegram API credentials in .env') 