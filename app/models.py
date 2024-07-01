# models.py

from sqlalchemy import Column, Integer, String
from app.database import Base  # Adjust import as per your folder structure

class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(String)
    type = Column(String)
