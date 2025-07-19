from fastapi import FastAPI
from router import router
from logger import logger

app = FastAPI(
    title="Fast Command API",
    description="Execute dynamic business commands via FastAPI.",
    version="1.0.0"
)

app.include_router(router)

logger.info("Fast Command API is up.")
