import config
import os
from discord.ext import commands

bot = commands.Bot(command_prefix = config.prefix)


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

    await bot.process_commands(context)


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
