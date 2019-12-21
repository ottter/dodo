import discord
import config
import os
import csv
import random
from discord.ext import commands

imgdir = './images'

def rename_folders(folder):
    # Example: rename_folders(f'{imgdir}/lights/')
    i = 0
    for filename in os.listdir(folder):
        dst = str(i) + ".png"
        src = folder + filename
        dst = folder + dst
        os.rename(src, dst)
        i += 1


class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command()
    async def lights(self, context):
        # rename_folders(f'{imgdir}/lights/')
        path, dirs, files = next(os.walk(f'{imgdir}/lights'))
        n = random.randint(0, len(files))
        await context.channel.send(file=discord.File(f'{imgdir}/lights/{n}.png'))

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command()
    async def jebrim(self, context):
        with open(f'{imgdir}/jebrim.csv') as f:
            reader = csv.reader(f)
            chosen_row = random.choice(list(reader))
            await context.channel.send(chosen_row[0])


def setup(bot):
    bot.add_cog(Users(bot))
