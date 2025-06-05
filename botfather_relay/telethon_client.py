from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from .config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE
import logging

SESSION_NAME = 'botfather_session'

class BotFatherSession:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

    async def start(self):
        await self.client.start(phone=TELEGRAM_PHONE)
        logging.info('Telethon client started and session established.')

    async def stop(self):
        await self.client.disconnect()
        logging.info('Telethon client disconnected.')

    async def send_message(self, entity, message):
        try:
            return await self.client.send_message(entity, message)
        except Exception as e:
            logging.error(f'Error sending message: {e}')
            raise 