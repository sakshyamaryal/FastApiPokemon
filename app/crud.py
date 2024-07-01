# crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Pokemon

async def get_pokemons(db: AsyncSession, name: str = None, type: str = None):
    query = select(Pokemon)
    if name:
        query = query.filter(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.filter(Pokemon.type.ilike(f"%{type}%"))
    result = await db.execute(query)
    return result.scalars().all()

async def create_pokemon(db: AsyncSession, name: str, image: str, type: str):
    pokemon = Pokemon(name=name, image=image, type=type)
    db.add(pokemon)
    await db.commit()
    return pokemon
