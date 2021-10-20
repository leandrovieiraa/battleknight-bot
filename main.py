# libs
import os
from dotenv import load_dotenv
from pathlib import Path
from models.config import Config
from models.routes import Routes
from bot.jobs import Jobs


# Load env variables
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

# Setup config
config = Config(
    server='s26-br', 
    username=os.getenv('PLAYER_USERNAME'), 
    password=os.getenv('PLAYER_PASSWORD')
)

# create routes
routes = Routes()

# Create jobs
jobs = Jobs()

# Login
jobs.login(config.server, routes.auth(), config.username, config.password)

# Load Character
character = jobs.load_character(config.server, routes.character())

# Do randon mission
jobs.go_to_mission(config.server, routes.world(), character)
