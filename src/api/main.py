import contextlib
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.api.routes import prescriptions, reminders, appointments, voice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/quickcare"
    redis_url: str = "redis://localhost:6379"
    environment: str = "development"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
redis_client: aioredis.Redis | None = None


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = await aioredis.from_url(settings.redis_url, decode_responses=True)
    app.state.redis = redis_client
    logger.info("Redis connected")
    yield
    await redis_client.close()
    await engine.dispose()
    logger.info("Connections closed")


app = FastAPI(
    title="QuickCare API",
    description="AI-powered NHS healthcare companion — multilingual prescription and appointment support",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(voice.router, prefix="/voice", tags=["Voice"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "QuickCare API"}
