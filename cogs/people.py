import re
import random
import config
from discord.ext import commands
import urllib
import discord

IMG_DIR = './images'    # Used in .csv method

def valid_host(host):
    for accepted_host in config.accepted_hosts:
        if host in accepted_host:
            return True
    
    return False

def valid_media_type(media_type):
    return media_type in config.accepted_media_types

def add_image(context, person):
    """ Tests the URL and adds to specific collection csv"""
    args = context.message.content.split(" ")

    parsed_url = urllib.parse.urlparse(args[1])
    host = parsed_url.hostname.split('.')[0]
    media_type = args[1].split('.')[-1]

    if not valid_host(host) and not valid_media_type(media_type):  # Tests for imgur image URL
        return context.send(f'Invalid URL, try again.')

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

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def people(self, context):
        """Stat count on People database"""
        collection = config.db['people']
        person_count = []
        count_dict = {}
        for person in collection.find({}, {'_id': 0, 'person': 1}):
            person_count.append(person['person'])
        for person in list(set(person_count)):
            count_dict[person] = person_count.count(person)
        person_print = ['`{0}: {1}`\t'.format(k.capitalize(), v) for k, v in sorted(count_dict.items())]
        await context.send('Current Image Totals:\n')
        await context.send(''.join(person_print))

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def lights(self, context):
        """Shows you the best of Lights473"""

        await random_image(context, 'lights')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_lights(self, context):
        """Add to the Lights collection"""

        await add_image(context, 'lights')

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['jeb'])
    async def jebrim(self, context):
        """Shows you the best of Jebrim"""

        await random_image(context, 'jebrim')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_jebrim(self, context):
        """Add to the Jebrim collection"""

        await add_image(context, 'jebrim')
        
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def mars(self, context):
        """Shows you the best of Marianna"""

        await random_image(context, 'mars')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_mars(self, context):
        """Add to the Marianna collection"""

        await add_image(context, 'mars')

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def pgt(self, context):
        """Shows you the best of Pgt"""

        await random_image(context, 'pgt')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_pgt(self, context):
        """Add to the Pgt collection"""

        await add_image(context, 'pgt')

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def corona(self, context):
        """Shows you the best Corona quotes"""

        await random_image(context, 'corona')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def add_corona(self, context):
        """Add to the Corona collection"""

        await add_image(context, 'corona')
    
    @commands.command(pass_context=True, alias='profile')
    async def profile(self, context: commands.Context, user: discord.User):
        profiles = config.db['profiles']
        profile = profiles.find_one({'_id': user.id})

        helper = discord.Embed(title=f'{user.display_name}\'{'' if use.display_name[-1] == 's' else 's'} Profile', color=0x00ff00)
        helper.set_thumbnail(url=user.avatar_url)
        helper.add_field(name='Bio', 
                        value=f"{profile['bio']}\n\nThis profile was written by {profile['author']}.", 
                        inline=False)

        await context.send(embed=helper)
    
    @commands.command(pass_context=True, alias='set_profile')
    async def set_profile(self, context: commands.Context, user: discord.User, *bio: str):
        if context.message.author.id in ['150125122408153088', '363762044396371970', '205144077144948737'] or context.message.author.id == user.id:
            profiles = config.db['profiles']
            profiles.update_one({'bio': ' '.join(bio), 'author': context.message.author.display_name}, {'$set': {'_id': user.id}}, upsert=True)

            await context.send(f'Added a profile for {user.display_name}.')

def setup(bot):
    bot.add_cog(People(bot))
