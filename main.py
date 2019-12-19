import discord
import config
from discord import Game
from discord.ext import commands

Bot = discord.Client()
bot = commands.Bot(command_prefix=config.bot_prefix, description=config.bot_description)

@bot.event
async def on_ready():

    print('-'*34)
    print('Logged in as: ', bot.user.name)
    print('Client ID:    ', bot.user.id)
    print('Local time:   ', config.server_time)
    print('-'*34)


@bot.event
async def on_message(context):
    message = str(context.content.lower())
    if context.author == bot.user:
        return

    if message.find('president trump') != -1:
        await context.channel.send('President Trump, the Impeached*')


if __name__ == '__main__':
    for extension in config.startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as err:
            exc = f'{type(err).__name__}: {err}'
            print(f'Failed to load extension {extension}\n{exc}')

    print('Attempting to log in...')

    try:
        bot.run(config.discord_token)
    except Exception as error:
        print('Discord: Unsuccessful login. Error: ', error)
        quit()