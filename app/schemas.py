from pydantic import BaseModel

class PokemonSchema(BaseModel):
    id: int
    name: str
    image: str
    type: str

    class Config:
        orm_mode = True
