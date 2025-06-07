# (File moved from botfather_relay/ to project root) 
from telethon import TelegramClient
from telethon.tl.types import User
from telethon.tl.custom import Button
from telethon.tl.custom.message import Message
import os
from dotenv import load_dotenv
import asyncio
import logging

# Configure logging
logger = logging.getLogger(__name__)

class BotFatherSession:
    def __init__(self):
        load_dotenv()
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_PHONE')
        self.session_name = os.getenv('TELETHON_SESSION_NAME', 'botfather_session')
        
        if not all([self.api_id, self.api_hash, self.phone]):
            raise ValueError("Missing required environment variables. Please check your .env file.")
        
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        self.botfather_entity = None

    async def start(self):
        """Start the client and ensure we're connected to BotFather."""
        logger.info("Starting Telegram client...")
        await self.client.start(phone=self.phone)
        self.botfather_entity = await self.client.get_entity('@BotFather')
        if not isinstance(self.botfather_entity, User):
            raise ValueError("Could not find BotFather entity")
        logger.info("Successfully connected to BotFather")

    async def stop(self):
        """Stop the client."""
        logger.info("Disconnecting from Telegram...")
        await self.client.disconnect()
        logger.info("Disconnected successfully")

    async def send_message(self, recipient: str, message: str) -> dict:
        """Send a message to BotFather and return the message details."""
        if not self.botfather_entity:
            raise RuntimeError("Client not started. Call start() first.")
        
        logger.info(f"Sending message to BotFather: {message}")
        message = await self.client.send_message(self.botfather_entity, message)
        logger.info("Message sent successfully")
        return {
            'id': message.id,
            'text': message.text
        }

    def _extract_buttons(self, message: Message) -> list:
        """Extract buttons from a message."""
        if not message.reply_markup:
            return None
            
        buttons = []
        if hasattr(message.reply_markup, 'rows'):
            for row in message.reply_markup.rows:
                row_buttons = []
                for button in row.buttons:
                    if hasattr(button, 'text'):
                        row_buttons.append(button.text)
                if row_buttons:
                    buttons.append(row_buttons)
        return buttons if buttons else None

    async def get_replies(self, from_entity: str, limit: int = 1) -> list:
        """Get the last N messages from BotFather."""
        if not self.botfather_entity:
            raise RuntimeError("Client not started. Call start() first.")
        
        logger.info(f"Fetching last {limit} replies from BotFather")
        messages = await self.client.get_messages(
            self.botfather_entity,
            limit=limit
        )
        logger.info(f"Successfully fetched {len(messages)} replies")
        
        return [{
            'id': msg.id,
            'text': msg.text,
            'buttons': self._extract_buttons(msg)
        } for msg in messages]

    async def click_button(self, msg_id: int = None, button_text: str = None, row: int = None, col: int = None) -> dict:
        """Click a button in a BotFather message.
        
        Args:
            msg_id: The ID of the message containing the button (default: last message)
            button_text: The text of the button to click (if using text-based selection)
            row: The row index of the button (if using position-based selection)
            col: The column index of the button (if using position-based selection)
            
        Returns:
            dict: Result of the button click containing:
                - id: Message ID
                - button: Button text or (row, col)
                - result: Result of the button press
                - status: "success" or "error"
        """
        if not self.botfather_entity:
            raise RuntimeError("Client not started. Call start() first.")
            
        if not (button_text or (row is not None and col is not None)):
            raise ValueError("Must specify either button_text or both row and col")
            
        try:
            # Get the message
            if msg_id is None:
                logger.info("No message ID specified, using last message")
                messages = await self.client.get_messages(self.botfather_entity, limit=1)
                if not messages:
                    return {
                        'id': None,
                        'button': button_text or f"({row}, {col})",
                        'result': "No messages found",
                        'status': "error"
                    }
                message = messages[0]
                msg_id = message.id
            else:
                message = await self.client.get_messages(self.botfather_entity, ids=msg_id)
                if not message:
                    return {
                        'id': msg_id,
                        'button': button_text or f"({row}, {col})",
                        'result': "Message not found",
                        'status': "error"
                    }
                
            # Check if message has buttons
            if not message.reply_markup:
                return {
                    'id': msg_id,
                    'button': button_text or f"({row}, {col})",
                    'result': "Message has no buttons",
                    'status': "error"
                }
                
            # Click the button
            if button_text:
                # Clean up button text (remove @ and make case-insensitive)
                clean_button_text = button_text.lstrip('@').lower()
                logger.info(f"Looking for button with text: {clean_button_text}")
                
                # Try to find the button by text
                found = False
                if hasattr(message.reply_markup, 'rows'):
                    for row_idx, row in enumerate(message.reply_markup.rows):
                        for col_idx, button in enumerate(row.buttons):
                            if hasattr(button, 'text') and button.text.lower() == clean_button_text:
                                logger.info(f"Found button at position ({row_idx}, {col_idx})")
                                # Click the button using the correct method
                                result = await message.click(data=button.data)
                                found = True
                                break
                        if found:
                            break
                
                if not found:
                    return {
                        'id': msg_id,
                        'button': button_text,
                        'result': f"Button with text '{button_text}' not found",
                        'status': "error"
                    }
                    
                button_info = button_text
            else:
                logger.info(f"Clicking button at position: ({row}, {col})")
                # Get the button at the specified position
                if not hasattr(message.reply_markup, 'rows') or row >= len(message.reply_markup.rows):
                    return {
                        'id': msg_id,
                        'button': f"({row}, {col})",
                        'result': f"Row {row} out of range",
                        'status': "error"
                    }
                    
                row_buttons = message.reply_markup.rows[row].buttons
                if col >= len(row_buttons):
                    return {
                        'id': msg_id,
                        'button': f"({row}, {col})",
                        'result': f"Column {col} out of range",
                        'status': "error"
                    }
                    
                button = row_buttons[col]
                result = await message.click(data=button.data)
                button_info = f"({row}, {col})"
                
            return {
                'id': msg_id,
                'button': button_info,
                'result': result.text if hasattr(result, 'text') else str(result),
                'status': "success"
            }
            
        except Exception as e:
            logger.error(f"Error clicking button: {e}")
            return {
                'id': msg_id,
                'button': button_text or f"({row}, {col})",
                'result': str(e),
                'status': "error"
            } 