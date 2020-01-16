import time
import datetime
from pymongo import MongoClient

server_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

# discord_token = 'NjU3MTE3MTQ5NjEyOTk4NjU3.XfsiSw.DMYcS8Mi2uSn4j9-wHzLD6V9RJk'   # Poli
DISCORD_TOKEN = 'NDM2MzMxMzg0MjQwNDcyMDc1.DhSvhA.S5Wr3spFv6bcNaR_fSnq8jPcKFk'   # Dodo

discord_game_played = 'Runescape'

OWM_TOKEN = 'a78bb1e133402c11c12db16f93a211dc'

MONGO_TOKEN = MongoClient("mongodb+srv://james:4nOrxGKx2CSvjoBX@cluster0-wm7ma.mongodb.net/test?retryWrites=true&w=majority")
db = MONGO_TOKEN.get_database('discord')

# document = {'_id': 1, 'home_loc': '4207400', 'unit': 'metric'}
# collection.insert_one(document)

# document = {'discord_id': 1}
# collection.create_index([{"discord_id": '1'}],unique=True)
# collection.update({'discord_id': 1},
#                   {"$set":{'home_loc': '4207400', 'unit': 'metric'}})

# results = collection.find({'discord_id': 0})
# for result in results:
#     print(result['unit'])

# results = collection.delete_one({'discord_id': 0})

# results = collection.update_one({'discord_id': 0}, {'$set':{'unit':'imperial'}})
