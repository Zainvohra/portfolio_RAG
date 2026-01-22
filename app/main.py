from dotenv import load_dotenv
load_dotenv()

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.routers import chat

from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

logger = structlog.get_logger()

app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "PulseAI Backend is running"}

@app.get("/")
async def root():
    return {"message": "PulseAI Backend API", "docs": "/docs"}
