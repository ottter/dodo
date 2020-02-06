import random
import config
import discord
from discord.ext import commands
import urllib.request
import json

def random_image():
    """ Returns a random Imgur URL from the selected file"""
    collection = config.db['xkcd']
    count = collection.count()

    random_selection = random.randint(1, count)
    image = collection.find({'_id': random_selection})

    for doc in image:
        return doc

class Xkcd(commands.Cog):
    """Channel-specific Quotes and memes"""
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def xkcd(self, context):
        doc = random_image()

        xkcd_embed = discord.Embed()
        xkcd_embed.set_author(name=f"#{doc['_id']} {doc['title']}")
        xkcd_embed.set_image(url=doc['img'])

        await context.send(embed=xkcd_embed)


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(alias=['xkcd_update'])
    async def update_xkcd(self, context):
        collection = config.db['xkcd']
        count = collection.count()

        with urllib.request.urlopen("https://xkcd.com/info.0.json") as url:
            data = json.loads(url.read().decode())
            num = data['num']

        for x in range(count, num):
            with urllib.request.urlopen(f'https://xkcd.com/{x}/info.0.json') as url:
                data = json.loads(url.read().decode())
                json_data = {"_id": data['num'], "title": data['title'], "sum": data['transcript'], "img": data['img']}
                collection.insert_one(json_data)

        await context.send('Updated `xkcd` database')


def setup(bot):
    bot.add_cog(Xkcd(bot))