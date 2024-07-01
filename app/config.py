from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv('DATABASE_URL')

    class Config:
        env_file = ".env"

# Create an instance of Settings
settings = Settings()
