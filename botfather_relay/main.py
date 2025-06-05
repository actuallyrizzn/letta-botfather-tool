import uvicorn
from fastapi import FastAPI
from botfather_relay.api.routes import router
from botfather_relay.utils.logging import setup_logging
from botfather_relay.telethon_client import BotFatherSession
from botfather_relay.config import HOST, PORT
import asyncio

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

if __name__ == "__main__":
    uvicorn.run("botfather_relay.main:app", host=HOST, port=PORT, reload=True) 