import os
import time
import datetime
from pymongo import MongoClient

server_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

discord_game_played = 'Runescape'

OWM_TOKEN = os.environ['OMW_API_KEY']

MONGO_TOKEN = MongoClient(f"{os.environ['MONGO_PASSWORD']}")
db = MONGO_TOKEN.get_database('discord')