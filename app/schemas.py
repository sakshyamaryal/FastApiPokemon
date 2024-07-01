from pydantic import BaseModel
from app.database import Base  # Adjust the import path as necessary

# Pydantic schema for Pokemon data
class PokemonBase(BaseModel):
    name: str
    image: str
    type: str

# Pydantic schema for creating a new Pokemon
class PokemonCreate(PokemonBase):
    pass

# Pydantic schema for Pokemon response with ORM mode enabled
class PokemonSchema(BaseModel):
    id: int
    name: str
    image: str
    type: str

    class Config:
        orm_mode = True
