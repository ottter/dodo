import re
import random
import config
from discord.ext import commands

IMG_DIR = './images'    # Used in .csv method

def add_image(context, person):
    """ Tests the URL and adds to specific collection csv"""
    args = context.message.content.split(" ")

    if not re.match('https?://i\.imgur\.com/[A-z0-9]+\.(png|jpg)/?', args[1]):  # Tests for imgur image URL
        return context.send('Direct Imgur links only.')

    collection = config.db['people']
    collection.update_one({'image_url': args[1]}, {'$set': {'person': person}}, upsert=True)    # Prevents duplicates
    return context.send(f'Added to the `{person}` collection')

    # # To use with .csv storage instead of in a database
    # with open(f'{IMG_DIR}/{person}.csv', 'r') as f:  # Tests for duplicate URLs
    #     reader = csv.reader(f)
    #     for r in reader:
    #         if args[1] == r[0]:
    #             return context.send(f'That image is already in: `{person}.csv`')
    #
    # with open(f'{img_dir}/{person}.csv', 'a') as f:  # Adds entry to the .csv if it passes RegEx & duplicate
    #     f.write(f'\n{args[1]}')
    #     return context.send(f'Added to the `{person}` collection')


def random_image(context, person):
    """ Returns a random Imgur URL from the selected file"""
    collection = config.db['people']
    images = collection.find({'person': person})
    row = []
    for image in images:
        row.append(image['image_url'])
    rand_img = random.choice(list(row))
    return context.channel.send(rand_img)


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

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_lights(self, context):
        """Add to the Lights collection"""

        await add_image(context, 'lights')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_jebrim(self, context):
        """Add to the Jebrim collection"""

        await add_image(context, 'jebrim')
        
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command()
    async def mars(self, context):
        """Shows you the best of Marianna"""

        await random_image(context, 'mars')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_mars(self, context):
        """Add to the Marianna collection"""

        await add_image(context, 'mars')

def setup(bot):
    bot.add_cog(People(bot))
