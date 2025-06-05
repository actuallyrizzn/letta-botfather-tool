from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from ..telethon_client import BotFatherSession
from .models import SendMessageRequest, SendMessageResponse, ErrorResponse
from ..config import API_BEARER_TOKEN
from typing import List
import logging
import time
from collections import defaultdict

router = APIRouter()

# Dependency to get BotFatherSession
botfather_session = BotFatherSession()

# Rate limiting: 10 requests per minute per client
RATE_LIMIT = 10
RATE_WINDOW = 60  # seconds
rate_limit_store = defaultdict(list)

async def verify_token(authorization: str = Header(None)):
    if not API_BEARER_TOKEN:
        return
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Invalid or missing bearer token')
    token = authorization.split(' ')[1]
    if token != API_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid bearer token')

async def rate_limit(request: Request):
    client_ip = request.client.host
    now = time.time()
    # Clean old entries
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if now - t < RATE_WINDOW]
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail='Rate limit exceeded')
    rate_limit_store[client_ip].append(now)

@router.post('/send_message', response_model=SendMessageResponse, responses={400: {'model': ErrorResponse}, 401: {'model': ErrorResponse}, 429: {'model': ErrorResponse}})
async def send_message(request: SendMessageRequest, _: None = Depends(verify_token), __: None = Depends(rate_limit)):
    try:
        # Forward message to BotFather
        entity = 'BotFather'
        sent_message = await botfather_session.send_message(entity, request.message)
        # Retrieve the 3 most recent replies (stub for now)
        replies = ["stub reply 1", "stub reply 2", "stub reply 3"]
        return SendMessageResponse(messages=replies)
    except Exception as e:
        logging.error(f"/send_message error: {e}")
        raise HTTPException(status_code=400, detail=str(e)) 