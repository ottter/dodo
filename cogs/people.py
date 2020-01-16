import re
import csv
import random
from discord.ext import commands

imgdir = './images'

def add_image(context, person):
    """ Tests the URL and adds to specific collection csv"""
    args = context.message.content.split(" ")

    if not re.match('https?://i\.imgur\.com/[A-z0-9]+\.(png|jpg)/?', args[1]):  # Tests for imgur image URL
        return context.send('Direct Imgur links only.')

    with open(f'{imgdir}/{person}.csv', 'r') as f:  # Tests for duplicate URLs
        reader = csv.reader(f)
        for r in reader:
            if args[1] == r[0]:
                return context.send(f'That image is already in: `{person}.csv`')

    with open(f'{imgdir}/{person}.csv', 'a') as f:  # Adds entry to the .csv if it passes RegEx & duplicate
        f.write(f'\n{args[1]}')
        return context.send(f'Added to the `{person}` collection')

def random_image(context, person):
    """ Returns a random Imgur URL from the selected file"""
    with open(f'{imgdir}/{person}.csv') as f:
        reader = csv.reader(f)
        chosen_row = random.choice(list(reader))
        return context.channel.send(chosen_row[0])


class People(commands.Cog):
    """Channel-specific Quotes and memes"""
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command()
    async def lights(self, context):
        """Shows you the best of Lights473"""

        await random_image(context, 'lights')

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command()
    async def jebrim(self, context):
        """Shows you the best of Jebrim"""

        await random_image(context, 'jebrim')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    async def add_lights(self, context):
        """Add to the Lights collection"""

        await add_image(context, 'lights')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    async def add_jebrim(self, context):
        """Add to the Jebrim collection"""

        await add_image(context, 'jebrim')

def setup(bot):
    bot.add_cog(People(bot))
