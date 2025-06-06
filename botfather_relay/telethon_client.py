from telethon import TelegramClient
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    FloodWaitError,
    UserDeactivatedError,
    SessionRevokedError
)
from .config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE
import logging
import asyncio
from typing import List, Optional
import time
import os
from dotenv import load_dotenv, set_key

SESSION_NAME = 'botfather_session'
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Define the path for caching the auth code
AUTH_CODE_FILE = 'auth_code.txt'

# Load environment variables from .env
load_dotenv()

class BotFatherSession:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
        self._last_message_id: Optional[int] = None
        self._is_authenticated = False

    async def start(self):
        try:
            if not self.client.is_connected():
                await self.client.connect()
            
            if not await self.client.is_user_authorized():
                await self.client.send_code_request(TELEGRAM_PHONE)
                logging.info('Authentication code sent. Please check your Telegram app.')
                # Check if cached auth code exists in .env
                cached_code = os.getenv('TELEGRAM_AUTH_CODE')
                if cached_code:
                    code = cached_code
                else:
                    code = input('Enter the code you received: ')
                    # Cache the code in .env
                    set_key('.env', 'TELEGRAM_AUTH_CODE', code)
                try:
                    await self.client.sign_in(TELEGRAM_PHONE, code)
                except SessionPasswordNeededError:
                    # If 2FA is enabled, prompt for password
                    password = input('Please enter your 2FA password: ')
                    await self.client.sign_in(password=password)
            else:
                self._is_authenticated = True
                
            logging.info('Telethon client started and session established.')
        except Exception as e:
            logging.error(f'Failed to start Telethon client: {e}')
            raise

    async def stop(self):
        try:
            if self.client.is_connected():
                await self.client.disconnect()
            self._is_authenticated = False
            logging.info('Telethon client disconnected.')
        except Exception as e:
            logging.error(f'Error during client shutdown: {e}')
            raise

    async def send_message(self, entity: str, message: str) -> dict:
        if not self._is_authenticated:
            raise RuntimeError("Client is not authenticated")

        for attempt in range(MAX_RETRIES):
            try:
                # Validate message
                if not message or len(message.strip()) == 0:
                    raise ValueError("Message cannot be empty")
                
                # Send message
                sent_message = await self.client.send_message(entity, message)
                self._last_message_id = sent_message.id
                
                # Wait briefly to ensure message is processed
                await asyncio.sleep(0.5)
                
                return {
                    'id': sent_message.id,
                    'text': sent_message.text,
                    'date': sent_message.date.isoformat()
                }
                
            except FloodWaitError as e:
                wait_time = e.seconds
                logging.warning(f'Rate limited. Waiting {wait_time} seconds.')
                await asyncio.sleep(wait_time)
                continue
                
            except (PhoneCodeInvalidError, UserDeactivatedError, SessionRevokedError) as e:
                logging.error(f'Authentication error: {e}')
                self._is_authenticated = False
                raise
                
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    logging.error(f'Failed to send message after {MAX_RETRIES} attempts: {e}')
                    raise
                await asyncio.sleep(RETRY_DELAY)
                continue

    async def get_replies(self, entity: str, limit: int = 3) -> List[dict]:
        if not self._is_authenticated:
            raise RuntimeError("Client is not authenticated")

        try:
            replies = []
            async for message in self.client.iter_messages(
                entity,
                limit=limit,
                min_id=self._last_message_id
            ):
                replies.append({
                    'id': message.id,
                    'text': message.text,
                    'date': message.date.isoformat()
                })
            return replies
        except Exception as e:
            logging.error(f'Error retrieving replies: {e}')
            raise 