import os
import time
import datetime
from pymongo import MongoClient

server_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

DISCORD_TOKEN = 'NDM2MzMxMzg0MjQwNDcyMDc1.Xm_4Xw.foUFkebL6a3Yleqs6ZLbCr5b-4s'

discord_game_played = 'Runescape'

OWM_TOKEN = os.environ['OMW_API_KEY']

COINMARKET_KEY = os.environ['CMC_API_KEY']

MONGO_TOKEN = MongoClient("mongodb+srv://james:QZ6X1NJfhG6JIjcq@cluster0-wm7ma.mongodb.net/test?retryWrites=true&w=majority")
db = MONGO_TOKEN.get_database('discord')

accepted_hosts = ['discord', 'imgur', 'youtube', 'gyazo']
accepted_media_types =['png', 'jpg', 'jpeg']
