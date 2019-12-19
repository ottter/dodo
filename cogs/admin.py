from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)  # _ use per _ seconds per user/channel/server #
    @commands.command(name='reload', hidden=True, pass_context=True)
    async def reload(self, context, module: str):
        admins = ['150125122408153088']
        if str(context.message.author.id) in admins:
            try:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
                await context.send('Reloaded')
            except Exception as err:
                print('{}: {}'.format(type(err).__name__, err))
                await context.send('Error: Did you use dot path (cogs.admin)?')
        else:
            await context.send('Admin Only')

def setup(bot):
    bot.add_cog(Admin(bot))