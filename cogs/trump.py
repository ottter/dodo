import discord
import config
from discord.ext import commands


class Trump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Trump(bot))
