from discord.ext import commands

admins = ['150125122408153088']

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, pass_context=True)
    async def reload(self, context, module: str):
        if str(context.message.author.id) in admins:
            try:
                self.bot.unload_extension(f'cogs.{module}')
                self.bot.load_extension(f'cogs.{module}')
                await context.send('Reloaded')
            except Exception as err:
                print('{}: {}'.format(type(err).__name__, err))
                await context.send(err)
        else:
            await context.send('Admin Only')

    @commands.command(hidden=True, pass_context=True)
    async def load(self, context, module: str):
        if str(context.message.author.id) in admins:
            try:
                self.bot.load_extension(f'cogs.{module}')
                await context.send('Reloaded')

            except Exception as err:
                print('{}: {}'.format(type(err).__name__, err))
                await context.send(err)
        else:
            await context.send('Admin Only')

    @commands.command(hidden=True, pass_context=True)
    async def unload(self, context, module: str):
        if str(context.message.author.id) in admins:
            try:
                self.bot.unload_extension(f'cogs.{module}')
                await context.send('Unloaded')
            except Exception as err:
                print('{}: {}'.format(type(err).__name__, err))
                await context.send('Error unloading cog')
        else:
            await context.send('Admin Only')


def setup(bot):
    bot.add_cog(Admin(bot))
