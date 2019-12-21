from discord.ext import commands
from discord import Game
import discord
import config

admins = ['150125122408153088']

class Admin(commands.Cog):
    """Basic bot admin level controls"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def reload(self, context, module: str):
        """Reload the specified cog [off then on]"""
        if str(context.message.author.id) in admins:
            try:
                self.bot.unload_extension(f'cogs.{module}')
                self.bot.load_extension(f'cogs.{module}')
                await context.send('Reloaded')
            except Exception as err:
                print('{}: {}'.format(type(err).__name__, err))
                await context.send(err)
        else:
            await context.send('Bot Admin Only')

    @commands.command(pass_context=True)
    async def load(self, context, module: str):
        """Loads the specified cog [on]"""
        if str(context.message.author.id) in admins:
            try:
                self.bot.load_extension(f'cogs.{module}')
                await context.send('Reloaded')

            except Exception as err:
                print('{}: {}'.format(type(err).__name__, err))
                await context.send(err)
        else:
            await context.send('Bot Admin Only')

    @commands.command(pass_context=True)
    async def unload(self, context, module: str):
        """Unloads the specified cog [off]"""
        if str(context.message.author.id) in admins:
            try:
                self.bot.unload_extension(f'cogs.{module}')
                await context.send('Unloaded')
            except Exception as err:
                print('{}: {}'.format(type(err).__name__, err))
                await context.send('Error unloading cog')
        else:
            await context.send('Bot Admin Only')

    @commands.command(pass_context=True)
    async def game(self, context):
        """Changes the 'game played' status message"""
        if str(context.message.author.id) in admins:
            user_input = context.message.content.split(' ', 1)
            if user_input[1] == 'default'.lower():
                return await self.bot.change_presence(activity=Game(name=config.discord_game_played))
            await self.bot.change_presence(activity=Game(name=user_input[1]))

    @commands.command(pass_context=True)
    async def admin(self, context):
        """Lists the possible admin controls"""
        if str(context.message.author.id) in admins:
            cog = ('Admin',)
            variable = ((x, y) for x in self.bot.cogs for y in cog if x == y)

            for x, y in variable:
                helper = discord.Embed(title='Admin Commands')
                for cmd in self.bot.get_cog(y).get_commands():
                    if not cmd.hidden:
                        helper.add_field(name=cmd.name, value=cmd.help, inline=False)

            await context.message.author.send('', embed=helper)
        else:
            await context.send('Bot Admin Only')


def setup(bot):
    bot.add_cog(Admin(bot))
