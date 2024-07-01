from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_pokemons, create_pokemon
from .schemas import PokemonCreate, PokemonSchema
from .database import get_db  # Ensure get_db is imported

router = APIRouter()

@router.get("/pokemons", response_model=list[PokemonSchema])
async def read_pokemons(name: str = None, type: str = None, db: AsyncSession = Depends(get_db)):
    pokemons = await get_pokemons(db, name, type)
    return pokemons

@router.post("/pokemons", response_model=PokemonSchema)
async def create_pokemon(pokemon: PokemonCreate, db: AsyncSession = Depends(get_db)):
    created_pokemon = await create_pokemon(db, pokemon.name, pokemon.image, pokemon.type)
    return created_pokemon
