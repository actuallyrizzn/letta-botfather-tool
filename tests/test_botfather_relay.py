import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from datetime import datetime, timedelta

from botfather_relay.main import app
from botfather_relay.telethon_client import BotFatherSession

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_rate_limit_store():
    # Clear the rate limit store before each test
    from botfather_relay.api import routes
    routes.rate_limit_store.clear()

@pytest.fixture
def mock_botfather_session():
    """Mock BotFather session for testing."""
    with patch('botfather_relay.api.routes.botfather_session') as mock:
        mock.client = MagicMock()
        mock.client.is_connected.return_value = True
        mock.client.is_user_authorized = AsyncMock(return_value=True)
        mock.send_message = AsyncMock()
        mock.get_replies = AsyncMock()
        mock.start = AsyncMock()
        mock.stop = AsyncMock()
        yield mock

@pytest.fixture
def auth_headers():
    """Provide authentication headers for testing."""
    return {'Authorization': 'Bearer valid_token'}

def test_send_message_success(mock_botfather_session, auth_headers):
    """Test successful message sending."""
    mock_botfather_session.get_replies.return_value = [
        {'text': 'Please choose a name for your bot.'},
        {'text': 'Please choose a username for your bot.'},
        {'text': 'Great! Your bot has been created.'}
    ]
    
    response = client.post(
        '/send_message',
        json={'message': '/newbot'},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert len(response.json()['messages']) == 3
    mock_botfather_session.send_message.assert_called_once_with('BotFather', '/newbot')

def test_send_message_validation(mock_botfather_session, auth_headers):
    """Test message validation."""
    # Test empty message
    response = client.post(
        '/send_message',
        json={'message': ''},
        headers=auth_headers
    )
    assert response.status_code == 422
    
    # Test message too long
    response = client.post(
        '/send_message',
        json={'message': 'a' * 4097},
        headers=auth_headers
    )
    assert response.status_code == 422
    
    # Test invalid message format
    response = client.post(
        '/send_message',
        json={'message': '!@#$%^&*()'},
        headers=auth_headers
    )
    assert response.status_code == 422

def test_rate_limit(mock_botfather_session, auth_headers):
    """Test rate limiting functionality."""
    # Send requests up to the rate limit
    for _ in range(10):
        response = client.post(
            '/send_message',
            json={'message': '/newbot'},
            headers=auth_headers
        )
        assert response.status_code == 200
    
    # Next request should be rate limited
    response = client.post(
        '/send_message',
        json={'message': '/newbot'},
        headers=auth_headers
    )
    assert response.status_code == 429

def test_bearer_token_auth(mock_botfather_session):
    """Test bearer token authentication."""
    # Test missing token
    response = client.post('/send_message', json={'message': '/newbot'})
    assert response.status_code == 401
    
    # Test invalid token
    response = client.post(
        '/send_message',
        json={'message': '/newbot'},
        headers={'Authorization': 'Bearer invalid_token'}
    )
    assert response.status_code == 401
    
    # Test valid token
    response = client.post(
        '/send_message',
        json={'message': '/newbot'},
        headers={'Authorization': 'Bearer valid_token'}
    )
    assert response.status_code == 200

def test_error_handling(mock_botfather_session, auth_headers):
    """Test various error scenarios."""
    # Test connection error
    mock_botfather_session.client.is_connected.return_value = False
    mock_botfather_session.start.side_effect = RuntimeError("Connection failed")
    
    response = client.post(
        '/send_message',
        json={'message': '/newbot'},
        headers=auth_headers
    )
    assert response.status_code == 500
    
    # Test message sending error
    mock_botfather_session.client.is_connected.return_value = True
    mock_botfather_session.send_message.side_effect = ValueError("Invalid message")
    
    response = client.post(
        '/send_message',
        json={'message': '/newbot'},
        headers=auth_headers
    )
    assert response.status_code == 400

def test_session_management(mock_botfather_session, auth_headers):
    """Test session management and reconnection."""
    # Test session reconnection
    mock_botfather_session.client.is_connected.return_value = False
    mock_botfather_session.start = AsyncMock()
    
    response = client.post(
        '/send_message',
        json={'message': '/newbot'},
        headers=auth_headers
    )
    
    assert mock_botfather_session.start.called
    assert response.status_code == 200

def test_telethon_client():
    """Test Telethon client initialization."""
    session = BotFatherSession()
    assert session.client is not None 