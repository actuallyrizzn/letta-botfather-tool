import os
from dotenv import load_dotenv
from typing import Optional
import logging

# Load environment variables
load_dotenv()

# Telegram API Configuration
TELEGRAM_API_ID: Optional[str] = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH: Optional[str] = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_PHONE: Optional[str] = os.getenv('TELEGRAM_PHONE')

# API Security
API_BEARER_TOKEN: Optional[str] = os.getenv('API_BEARER_TOKEN')

# Server Configuration
HOST: str = os.getenv('HOST', '127.0.0.1')
PORT: int = int(os.getenv('PORT', '57431'))

# Rate Limiting
RATE_LIMIT: int = int(os.getenv('RATE_LIMIT', '10'))
RATE_WINDOW: int = int(os.getenv('RATE_WINDOW', '60'))

# Logging Configuration
LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def validate_config():
    """Validate the configuration and raise appropriate errors if invalid."""
    missing_vars = []
    
    # Check required Telegram credentials
    if not TELEGRAM_API_ID:
        missing_vars.append('TELEGRAM_API_ID')
    if not TELEGRAM_API_HASH:
        missing_vars.append('TELEGRAM_API_HASH')
    if not TELEGRAM_PHONE:
        missing_vars.append('TELEGRAM_PHONE')
    
    if missing_vars:
        raise RuntimeError(
            f'Missing required Telegram API credentials in .env: {", ".join(missing_vars)}'
        )
    
    # Validate numeric values
    try:
        if not isinstance(PORT, int) or PORT < 1 or PORT > 65535:
            raise ValueError(f'Invalid PORT value: {PORT}. Must be between 1 and 65535.')
    except ValueError as e:
        raise RuntimeError(f'Configuration error: {str(e)}')
    
    # Validate rate limiting configuration
    if RATE_LIMIT < 1:
        raise RuntimeError('RATE_LIMIT must be greater than 0')
    if RATE_WINDOW < 1:
        raise RuntimeError('RATE_WINDOW must be greater than 0')
    
    # Log configuration status
    logging.info('Configuration validated successfully')
    logging.info(f'Server will run on {HOST}:{PORT}')
    if API_BEARER_TOKEN:
        logging.info('API Bearer token authentication is enabled')
    else:
        logging.warning('API Bearer token authentication is disabled')

# Validate configuration on module import
validate_config() 