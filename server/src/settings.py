import os
from dotenv import load_dotenv

# Loads all the necessary settings from .env

load_dotenv()

DISCORD_API_SECRET = os.getenv('DISCORD_API_TOKEN')