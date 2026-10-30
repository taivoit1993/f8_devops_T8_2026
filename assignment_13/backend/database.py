import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgrespassword@localhost:5432/devops_db"
)

# Configure SSL connection arguments (needed for AWS RDS / cloud databases)
connect_args = {}
ssl_mode = os.getenv("DB_SSL_MODE")
if ssl_mode:
    if ssl_mode.lower() in ("require", "true", "1"):
        connect_args["ssl"] = "require"
    elif ssl_mode.lower() in ("false", "disable", "0"):
        connect_args["ssl"] = False
elif "rds.amazonaws.com" in DATABASE_URL:
    connect_args["ssl"] = "require"

# Create async engine for PostgreSQL
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    future=True,
    connect_args=connect_args
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base model
Base = declarative_base()

# FastAPI dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
