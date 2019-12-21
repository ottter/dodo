import config
import json
import time
import os
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

    if message.find('president trump') != -1:
        await context.channel.send('President Trump, the Impeached*')

    await bot.process_commands(context)

@bot.event
async def on_guild_join(guild):
    # Custom prefixes on a per-server basis in order to prevent command overlap
    with open('./files/prefixes.json', 'r') as file:
        prefixes = json.load(file)
    prefixes[str(guild.id)] = '.'
    with open('./files/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

    # TODO: Create server join message

@bot.event
async def on_guild_remove(guild):
    # Removes the custom prefix from prefixes.json
    with open('./files/prefixes.json', 'r') as file:
        prefixes = json.load(file)
    prefixes.pop(str(guild.id))
    with open('./files/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

@bot.command(alias='idm_prefix')
async def change_prefix(context, prefix):
    # Custom prefixes on a per-server basis in order to prevent command overlap
    # TODO: Make this an admin only command
    # TODO: Change prefix quantifier (right word?) to utilize RegEx for non-alphanumeric keyboard characters
    if len(prefix) == 1:
        with open('./files/prefixes.json', 'r') as file:
            prefixes = json.load(file)
        prefixes[str(context.guild.id)] = prefix
        with open('./files/prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)
        await context.send(f'Prefix changed to: {prefix}')
    else:
        await context.send(f'Entry is not a valid prefix')


def load_extensions():
    for filename in os.listdir('./cogs'):
        cog = filename[:-3]
        if filename.endswith('.py'):
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
        bot.run(config.discord_token)
    except Exception as error:
        print('Discord: Unsuccessful login. Error: ', error)
        quit()

if __name__ == '__main__':
    log_in()
