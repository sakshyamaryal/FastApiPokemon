from sqlalchemy.future import select
from sqlalchemy.orm import Session
from . import models, schemas

async def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Pokemon).offset(skip).limit(limit))
    return result.scalars().all()

async def create_pokemon(db: Session, pokemon: schemas.PokemonCreate):
    db_pokemon = models.Pokemon(**pokemon.dict())
    db.add(db_pokemon)
    await db.commit()
    await db.refresh(db_pokemon)
    return db_pokemon

async def get_pokemon_by_name(db: Session, name: str):
    result = await db.execute(select(models.Pokemon).where(models.Pokemon.name == name))
    return result.scalars().first()
