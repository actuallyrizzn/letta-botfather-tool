import uvicorn
from fastapi import FastAPI, Request
from botfather_relay.api.routes import router
from botfather_relay.utils.logging import setup_logging
from botfather_relay.telethon_client import BotFatherSession
from botfather_relay.config import HOST, PORT
from botfather_relay.api.models import ErrorResponse
import asyncio
import logging

app = FastAPI()
app.include_router(router)

botfather_session = BotFatherSession()

@app.on_event("startup")
async def startup_event():
    setup_logging()
    await botfather_session.start()

@app.on_event("shutdown")
async def shutdown_event():
    await botfather_session.stop()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return ErrorResponse(error=str(exc))

if __name__ == "__main__":
    uvicorn.run("botfather_relay.main:app", host=HOST, port=PORT) 