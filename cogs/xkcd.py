from discord.ext import commands
import urllib.request
import discord
import random
import config
import json

# Source data: https://xkcd.com/json.html

def xkcd_count():
    """ Gets the total xkcd comics posted"""    # This is different than total in collection
    with urllib.request.urlopen("https://xkcd.com/info.0.json") as url:
        data = json.loads(url.read().decode())
        return data['num']

def xkcd_random(self, context):
    """ Returns a random xkcd"""
    count = self.collection.count()
    rnd = random.randint(1, count)
    selection = self.collection.find({'_id': rnd})

    for doc in selection:
        return xkcd_output(context, doc)

def xkcd_specific(self, context, num):
    """ Returns a specific numbered xkcd"""
    image = self.collection.find({'_id': num})

    for doc in image:
        return xkcd_output(context, doc)

def xkcd_latest(context):
    """ Gets the latest xkcd comic posted"""
    with urllib.request.urlopen("https://xkcd.com/info.0.json") as url:
        data = json.loads(url.read().decode())
        doc = {'_id': data['num'], 'title': data['title'], 'sum': data['alt'], 'img': data['img']}
        return xkcd_output(context, doc)

def xkcd_output(context, doc):
    """ Converts document to discord embed"""
    xkcd_embed = discord.Embed(color=0x16e40c)
    xkcd_embed.set_author(name=f"#{doc['_id']} - {doc['title']}", url=f"https://xkcd.com/{doc['_id']}/")
    xkcd_embed.set_image(url=doc['img'])
    xkcd_embed.set_footer(text=f"{doc['sum']}")
    return context.send(embed=xkcd_embed)

class xkcd(commands.Cog):
    """ Provides user with random and relevant xkcd comics"""
    def __init__(self, bot):
        self.bot = bot
        self.collection = config.db['xkcd']

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def xkcd(self, context):
        """ Provides user with random and relevant xkcd comics
        .xkcd       Random image
        .xkcd [#]   Specific image
        .xkcd [txt] Find most relevant image"""
        args = context.message.content.lower().split(" ", 1)

        if len(args) == 1:
            return await xkcd_random(self, context)

        if args[1] == '404':
            return  # I bet you think you're so clever

        if args[1] == 'latest':
            return await xkcd_latest(context)

        if int(args[1]) in range(1, xkcd_count()):
            num = int(args[1])
            return await xkcd_specific(self, context, num)

        return


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['xkcd_update'])
    async def update_xkcd(self, context):
        """ Updates the database with any missing entries"""
        # +1 to compensate for 0
        count = self.collection.count() + 1
        num = xkcd_count() + 1

        if count == num:
            return await context.send(f'No new comics to update')

        for x in range(count, num):
            with urllib.request.urlopen(f'https://xkcd.com/{x}/info.0.json') as url:
                data = json.loads(url.read().decode())
                json_data = {"_id": data['num'], "title": data['title'], "sum": data['alt'], "img": data['img']}
                self.collection.insert_one(json_data)

        await context.send(f'Updated `xkcd` database with `{num - count}` new image(s)')


def setup(bot):
    bot.add_cog(xkcd(bot))