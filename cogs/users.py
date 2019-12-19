import discord
import config
import os
import random
from discord.ext import commands

imgdir = './images'

def rename_folders(folder):
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

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def lights(self, context):
        # rename_folders(f'{imgdir}/lights/')
        path, dirs, files = next(os.walk(f'{imgdir}/lights'))
        file_count = len(files) - 1
        n = random.randint(0, file_count)
        await context.channel.send(file=discord.File(f'{imgdir}/lights/{n}.png'))


def setup(bot):
    bot.add_cog(Users(bot))
