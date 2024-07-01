import aiohttp  # Import the aiohttp module for making async HTTP requests
import asyncio  # Import the asyncio module for async programming
from app.database import SessionLocal, init_db  # Import the session and init_db function
from app.crud import create_pokemon  # Import the create_pokemon function
from app.schemas import PokemonCreate  # Import the PokemonCreate schema

# Fetch data from a given URL
async def fetch_pokemon(session, url):
    async with session.get(url) as response:
        return await response.json()

# Main function to fetch and store Pokemon data
async def main():
    await init_db()  # Initialize the database
    async with aiohttp.ClientSession() as session:
        url = 'https://pokeapi.co/api/v2/pokemon?limit=100'
        pokemons = await fetch_pokemon(session, url)

        async with SessionLocal() as db:
            for poke in pokemons['results']:
                poke_detail = await fetch_pokemon(session, poke['url'])
                pokemon = PokemonCreate(
                    name=poke_detail['name'],
                    image=poke_detail['sprites']['front_default'],
                    type=[t['type']['name'] for t in poke_detail['types']]
                )
                await create_pokemon(db, pokemon)

# Run the main function
asyncio.run(main())
