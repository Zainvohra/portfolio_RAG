from dotenv import load_dotenv
load_dotenv()

import structlog
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.routers import chat

from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

logger = structlog.get_logger()

app.include_router(chat.router)
