from fastapi import FastAPI
from contextlib import asynccontextmanager

from config_db import create_db_tables
from routes import banner_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(
    title="MemoCloud API",
    lifespan=lifespan
)

app.include_router(banner_router)