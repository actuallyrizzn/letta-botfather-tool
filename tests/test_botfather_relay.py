import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from botfather_relay.main import app
from botfather_relay.telethon_client import BotFatherSession

client = TestClient(app)

@pytest.fixture
def mock_botfather_session():
    with patch('botfather_relay.api.routes.botfather_session') as mock:
        mock.send_message = AsyncMock(return_value=None)
        mock.client.iter_messages = AsyncMock()
        mock.client.iter_messages.return_value = [
            AsyncMock(text='reply 1'),
            AsyncMock(text='reply 2'),
            AsyncMock(text='reply 3')
        ]
        yield mock

def test_send_message(mock_botfather_session):
    response = client.post('/send_message', json={'message': '/newbot'})
    assert response.status_code == 200
    data = response.json()
    assert 'messages' in data
    assert data['messages'] == ['reply 1', 'reply 2', 'reply 3']

def test_rate_limit(mock_botfather_session):
    # Send requests up to the rate limit
    for _ in range(10):
        response = client.post('/send_message', json={'message': '/newbot'})
        assert response.status_code == 200
    # The next request should be rate limited
    response = client.post('/send_message', json={'message': '/newbot'})
    assert response.status_code == 429

def test_bearer_token_auth(mock_botfather_session):
    # Test missing token
    response = client.post('/send_message', json={'message': '/newbot'})
    assert response.status_code == 401
    # Test invalid token
    response = client.post('/send_message', json={'message': '/newbot'}, headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    # Test valid token (assuming API_BEARER_TOKEN is set in .env)
    response = client.post('/send_message', json={'message': '/newbot'}, headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 200

def test_error_handling(mock_botfather_session):
    # Simulate an exception in send_message
    mock_botfather_session.send_message.side_effect = Exception('Test error')
    response = client.post('/send_message', json={'message': '/newbot'})
    assert response.status_code == 400
    data = response.json()
    assert 'error' in data
    assert data['error'] == 'Test error' 