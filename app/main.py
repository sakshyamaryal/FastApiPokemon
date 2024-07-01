from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from sqlalchemy.future import select
from typing import List
import aiohttp
from .models import Base, Pokemon
from .database import get_db
from .schemas import PokemonSchema
from .config import settings

# Create the FastAPI instance
app = FastAPI()

# Initialize the database engine
engine = create_async_engine(settings.database_url, echo=True)

# Create a sessionmaker factory for database sessions
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Database dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Pydantic schema for Pokemon data
class PokemonBase(BaseModel):
    name: str
    image: str
    type: str

# Pydantic schema for creating a new Pokemon
class PokemonCreate(PokemonBase):
    pass



# Function to fetch data from the PokeAPI
async def fetch_data():
    url = "https://pokeapi.co/api/v2/pokemon?limit=100"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Function to store data in the database
async def store_data(db: AsyncSession):
    data = await fetch_data()
    for item in data['results']:
        # Fetch additional details for each Pokemon
        async with aiohttp.ClientSession() as session:
            async with session.get(item['url']) as response:
                details = await response.json()
                pokemon = Pokemon(
                    name=item['name'],
                    image=details['sprites']['front_default'],
                    type=details['types'][0]['type']['name']
                )
                db.add(pokemon)
    await db.commit()

# Event handler to create tables and fetch initial data on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        await store_data(session)

# Endpoint to get the list of Pokemons
@app.get("/api/v1/pokemons", response_model=List[PokemonSchema])
async def get_pokemons(name: str = None, type: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Pokemon)
    if name:
        query = query.filter(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.filter(Pokemon.type.ilike(f"%{type}%"))
    result = await db.execute(query)
    return result.scalars().all()

