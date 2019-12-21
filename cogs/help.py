import discord
from discord.ext import commands

class Help(commands.Cog):
    """Lists all cogs and commands"""

    def __init__(self, client):
        self.client = client

    # TODO: Add descriptions to all relevant commands and classes
    # TODO: Hide any irrelevant commands and classes from appearing
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name='help', pass_context=True, brief='help command')
    async def help(self, context, *cog):
        """Lists all cogs and commands"""

        try:
            if not cog:
                helper = discord.Embed(title='Cog Help',
                                       description=f'Use `.help *cog*` for more information')
                cogs_desc = ''

                for x in self.client.cogs:
                    cogs_desc += f'{x} - {self.client.cogs[x].__doc__}\n'

                helper.add_field(name='Cogs', value=cogs_desc[0:len(cogs_desc) - 1], inline=False)
                command_desc = ''

                for command_call in self.client.walk_commands():
                    if not command_call.cog_name and not command_call.hidden:
                        command_desc += f'{command_call.name} - {command_call.help}\n'

                helper.add_field(name='Misc Commands', value=command_desc[0:len(command_desc) - 1], inline=False)

                await context.message.author.send('', embed=helper)
                await context.message.add_reaction(emoji='✉')
            else:
                if len(cog) > 1:
                    helper = discord.Embed(description='Error! Too many requests', color=discord.Color.red())
                    await context.message.author.send('', embed=helper)

                else:
                    found = False
                    variable = ((x, y) for x in self.client.cogs for y in cog if x == y)
                    cmd_desc = self.client.cogs[cog[0]].__doc__

                    for x, y in variable:
                        helper = discord.Embed(title=f'{cog[0]} Command Listing', description=cmd_desc)
                        for cmd in self.client.get_cog(y).get_commands():
                            if not cmd.hidden:
                                helper.add_field(name=cmd.name, value=cmd.help, inline=False)
                        found = True

                    if not found:
                        helper = discord.Embed(description=f'Error! The {cog[0]} cog can not be found',
                                               color=discord.Color.red())

                    await context.message.author.send('', embed=helper)
                    await context.message.add_reaction(emoji='✉')
        except:
            pass


def setup(client):
    client.add_cog(Help(client))