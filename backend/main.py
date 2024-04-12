import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import chat_ai, mongodb_crud, image_ai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Nutrition AI",
    description="APIs for Nutrition AI",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_ai.router, prefix="/chat_ai", tags=["chat_ai"])
app.include_router(mongodb_crud.router, prefix="/mongo_db", tags=["mongo_db"])
app.include_router(image_ai.router, prefix="/image_ai", tags=["image_ai"])