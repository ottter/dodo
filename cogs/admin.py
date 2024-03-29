from discord.ext import commands
from discord import Game
import discord
import config
import json

admins = ['150125122408153088', '363762044396371970', '205144077144948737']

class Admin(commands.Cog):
    """Basic bot admin-level controls"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alias='add_alias')
    async def add_alias(self, context, user: discord.User, *alias):
        if str(context.message.author.id) in admins or user.id == context.message.author.id:
            if len(alias) > 1:
                await context.send('The alias must be a single word.')
                return 
            
            config.db['aliases'].update_one({'_id': user.id}, {'$addToSet': {'aliases': ' '.join(alias)}}, upsert=True)

            await context.send('Successfully added alias.')

    @commands.command(alias='unban_saj')
    async def unban_saj(self, context):
        if not str(context.message.author.id) in admins:
            return

        user = await self.bot.fetch_user(328043851891605506)
        try:
            await context.guild.unban(user)
        except:
            pass

        member = self.bot.get_user_info('328043851891605506')
        channel = await member.create_dm()

        link = await context.channel.create_invite(max_age=300)
        await channel.send(link)
        
        for role in context.guild.roles:
            if role.name in ['Philosopher', 'OG', 'Current WORST poster', 'Current BEST Pogrammer', 'Big Stonker', 'Preppy muslim', 'SUPER TAXPAYER (100K+)']:
                try:
                    await member.add_roles(role)
                except:
                    continue

    @commands.command()
    async def unban(self, context, user_id):
        # if not str(context.message.author.id) in admins:
        #     return

        philosopho = 563549980439347201
        print(context.guild.id)
        if context.guild.id != philosopho:
            print('unban message sent from wrong channel')
            return

        common_users = {
            "elena": 209385907101368322,
            "morgan": 273532188803203072,
            "saj": 328043851891605506,
            "swims": 193427271992868864,
            "miles": 149187078981287936,
            "zin": 240046314321084417,
        }
        if user_id == 'me':
            user_id = context.message.author.id

        if user_id in common_users:
            user_id = common_users[user_id]
        user = await self.bot.fetch_user(user_id)
        try:
            await context.guild.unban(user)
        except:
            pass

        channel = await user.create_dm()
        link = await context.channel.create_invite(max_age=1200)
        await channel.send(link)
        print(f'attempt to unban: {user_id}, aka {user}')
        
    @commands.command(alias='dodo_prefix')
    async def change_prefix(self, context, prefix):
        """Custom prefixes on a per-server basis in order to prevent command overlap"""
        # TODO: Change prefix quantifier (right word?) to utilize RegEx for non-alphanumeric keyboard characters
        if str(context.message.author.id) in admins:
            if len(prefix) == 1:
                with open('./files/prefixes.json', 'r') as file:
                    prefixes = json.load(file)
                prefixes[str(context.guild.id)] = prefix
                with open('./files/prefixes.json', 'w') as file:
                    json.dump(prefixes, file, indent=4)
                await context.send(f'Prefix changed to: {prefix}')
            else:
                await context.send(f'Entry is not a valid prefix')

    @commands.command(pass_context=True)
    async def reload(self, context, module: str):
        """Reload the specified cog [off then on]"""
        if str(context.message.author.id) in admins:
            try:
                self.bot.reload_extension(f'cogs.{module}')
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

    @commands.command(hidden=True)
    async def shutdown(self, context):
        if str(context.message.author.id) in admins:
            print('Shutting down...')
            await self.bot.logout()

def setup(bot):
    bot.add_cog(Admin(bot))
