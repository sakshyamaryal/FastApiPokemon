# Pokemon API

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd pokemon_api
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup environment variables**:
    Create a `.env` file in the root directory with the following content:
    ```
    DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>/<database>
    ```

5. **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the API**:
    Open your browser and go to `http://127.0.0.1:8000/api/v1/pokemons`.

## Endpoints

- **GET /api/v1/pokemons**: Get list of Pokemons with optional filtering by name and type.
- **GET /api/v1/pokemons?name=<name>&type=<type>**: Get filtered list of Pokemons.

- **GET http://127.0.0.1:8000/api/v1/pokemons?name=pikachu

## Additional Information

- The PokeAPI is called only once to fetch the list of Pokemons, which are then stored in the PostgreSQL database. All subsequent requests are served from the database.
# FastApiPokemon
