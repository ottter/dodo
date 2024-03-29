import config
import json
import time
import os
import discord
from discord.ext import commands


def get_prefix(client, message):
    try:
        with open('./files/prefixes.json', 'r') as file:
            prefixes = json.load(file)
        return prefixes[str(message.guild.id)]
    except:
        return '.'


bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command('help')

intents = discord.Intents.default()
intents.members = True


@bot.event
async def on_ready():

    print('-'*34)
    print('Logged in as: ', bot.user.name)
    print('Client ID:    ', bot.user.id)
    print('Local time:   ', config.server_time)
    print('-'*34)


@bot.command(hidden=True, pass_context=True)
async def ping(context):
    before = time.monotonic()
    message = await context.channel.send("Pong!")
    server_ping = f'Ping: {int((time.monotonic() - before) * 1000)}ms'

    await message.edit(content=server_ping)


@bot.event
async def on_message(context):
    message = str(context.content.lower())

    if context.author == bot.user:
        return

    if message.startswith('!saj'):
        await context.channel.send("I am here to inform you that Sajiel, developer of the #4 Dungeoneering software (with "
                                   "3500 unique downloads!), has a girlfriend, drives a Camry, is a Comp Sci graduate "
                                   "with six figure job, challenged Lights to a keyrace for the Lights Philsophy server, "
                                   "is buying a house in upstate New York (ask for pics), and is definitely not fat."
                                   "\nThanks for asking!")
    if message.find('!co2') != -1:
        await context.channel.send('Also CO2 is good for plants, meaning more CO2 means more life-sustaining oxygen '
                                   'and thus increase in agriculture as plants grow faster, more food, etc.')

    await bot.process_commands(context)


@bot.event
async def on_guild_join(guild):
    # TODO: Create server join message
    # Custom prefixes on a per-server basis in order to prevent command overlap
    with open('./files/prefixes.json', 'r') as file:
        prefixes = json.load(file)
    prefixes[str(guild.id)] = "."
    with open('./files/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@bot.event
async def on_guild_remove(guild):
    # Removes the custom prefix from prefixes.json when bot is removed from a server
    # TODO: Get this to work with extensions
    with open('./files/prefixes.json', 'r') as file:
        prefixes = json.load(file)
    prefixes.pop(str(guild.id))
    with open('./files/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@bot.event
async def on_member_remove(member):
    philoco = 563549980439347201
    welcome = 703752970894049320
    if member.guild.id == philoco:
        channel = bot.get_channel(welcome)
        message = f'Cya {member} you dummy'
        await channel.send(message)


def load_extensions():
    # Loads all of the extensions. Note: check iDM if I branch out to multiple folders
    exclusion_list = []
    for filename in os.listdir('./cogs'):
        cog = filename[:-3]
        if filename.endswith('.py') and cog not in exclusion_list:
            try:
                bot.load_extension(f'cogs.{cog}')
                print(f'Loaded extension: {cog}')
            except Exception as err:
                exc = f'{type(err).__name__}: {err}'
                print(f'Failed to load extension {cog}\n{exc}')


def log_in():
    load_extensions()
    print('Attempting to log in...')
    try:
        bot.run(config.DISCORD_TOKEN)
    except Exception as error:
        print('Discord: Unsuccessful login. Error: ', error)
        quit()


if __name__ == '__main__':
    log_in()
