import pytest
import os
from unittest.mock import patch
from botfather_relay.config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_PHONE,
    API_BEARER_TOKEN
)

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        'TELEGRAM_API_ID': '12345',
        'TELEGRAM_API_HASH': 'test_hash',
        'TELEGRAM_PHONE': '+1234567890',
        'API_BEARER_TOKEN': 'test_token',
        'HOST': '127.0.0.1',
        'PORT': '57431',
        'LOG_LEVEL': 'DEBUG'
    }):
        yield

@pytest.fixture
def test_config():
    """Provide test configuration values."""
    return {
        'api_id': TELEGRAM_API_ID,
        'api_hash': TELEGRAM_API_HASH,
        'phone': TELEGRAM_PHONE,
        'bearer_token': API_BEARER_TOKEN
    }

@pytest.fixture
def mock_telegram_client():
    """Mock Telegram client for testing."""
    with patch('telethon.TelegramClient') as mock:
        mock.return_value.is_connected.return_value = True
        mock.return_value.is_user_authorized.return_value = True
        yield mock

@pytest.fixture
def mock_async_sleep():
    """Mock asyncio.sleep to speed up tests."""
    with patch('asyncio.sleep') as mock:
        yield mock

@pytest.fixture(autouse=True, scope='session')
def patch_api_bearer_token():
    with patch('botfather_relay.config.API_BEARER_TOKEN', 'valid_token'), \
         patch('botfather_relay.api.routes.API_BEARER_TOKEN', 'valid_token'):
        yield 