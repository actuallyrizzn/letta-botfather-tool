from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from ..telethon_client import BotFatherSession
from .models import SendMessageRequest, SendMessageResponse, ErrorResponse
from ..config import API_BEARER_TOKEN
from typing import List, Optional
import logging
import time
from collections import defaultdict
import asyncio

router = APIRouter()

# Dependency to get BotFatherSession
botfather_session = BotFatherSession()

# Rate limiting: 10 requests per minute per client
RATE_LIMIT = 10
RATE_WINDOW = 60  # seconds
rate_limit_store = defaultdict(list)

async def verify_token(authorization: str = Header(None)):
    """Verify the bearer token."""
    if not API_BEARER_TOKEN:
        return
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or missing bearer token'
        )
    token = authorization.split(' ')[1]
    if token != API_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid bearer token'
        )
    return token

async def rate_limit(request: Request):
    """Check if the request is within rate limits."""
    client_ip = request.client.host
    now = time.time()
    
    # Clean old entries
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if now - t < RATE_WINDOW]
    
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f'Rate limit exceeded. Maximum {RATE_LIMIT} requests per {RATE_WINDOW} seconds.'
        )
    
    rate_limit_store[client_ip].append(now)

async def ensure_session():
    """Ensure the BotFather session is connected and authorized."""
    try:
        if not botfather_session.client.is_connected():
            await botfather_session.start()
        elif not await botfather_session.client.is_user_authorized():
            await botfather_session.start()
    except Exception as e:
        logging.error(f"Error ensuring session: {e}")
        raise RuntimeError("Failed to establish session with BotFather")

@router.post(
    '/send_message',
    response_model=SendMessageResponse,
    responses={
        400: {'model': ErrorResponse},
        401: {'model': ErrorResponse},
        429: {'model': ErrorResponse},
        500: {'model': ErrorResponse}
    }
)
async def send_message(
    request: SendMessageRequest,
    token: str = Depends(verify_token),
    _: None = Depends(rate_limit)
):
    """Send a message to BotFather and get the response."""
    try:
        # Ensure session is connected and authorized
        await ensure_session()
        
        # Forward message to BotFather
        entity = 'BotFather'
        sent_message = await botfather_session.send_message(entity, request.message)
        
        # Wait briefly to ensure BotFather has time to respond
        await asyncio.sleep(1)
        
        # Retrieve the replies
        replies = await botfather_session.get_replies(entity, limit=3)
        
        if not replies:
            logging.warning("No replies received from BotFather")
            return SendMessageResponse(messages=[])
        
        return SendMessageResponse(messages=[reply['text'] for reply in replies])
        
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        logging.error(f"Runtime error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    except Exception as e:
        logging.error(f"Unexpected error in /send_message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    try:
        await botfather_session.stop()
    except Exception as e:
        logging.error(f"Error during shutdown: {e}") 