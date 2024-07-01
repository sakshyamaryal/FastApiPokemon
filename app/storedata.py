import aiohttp
from .database import SessionLocal
from .models import Pokemon

# Function to fetch Pokemon data from PokeAPI
async def fetch_data():
    url = "https://pokeapi.co/api/v2/pokemon?limit=100"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Function to store data in the database
async def store_data():
    try:
        async with SessionLocal() as db:
            data = await fetch_data()
            for item in data['results']:
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
            print("Data stored successfully.")
    except Exception as e:
        print(f"Error storing data: {str(e)}")

# This block ensures the data is stored when this module is run directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(store_data())
