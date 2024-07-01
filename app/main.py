from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .database import get_db
from .models import Base, Pokemon
from .config import settings
from .api import router
from .storedata import store_data
import asyncio

# Initialize the FastAPI instance
app = FastAPI()

# Initialize the database engine
engine = create_async_engine(settings.database_url, echo=True)

# Create a sessionmaker factory for database sessions
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Database dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Event handler to create tables on startup and store initial data
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await store_data()

# Include router
app.include_router(router, prefix="/api/v1")  # Specify the prefix for API versioning

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
