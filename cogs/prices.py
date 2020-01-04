from discord.ext import commands
from urllib.request import urlopen
import urllib.request
import urllib.error
import sqlite3
import discord
import config
import json


class Prices(commands.Cog):
    """Crypto and Stock prices"""
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='stocks', aliases=['stonks', 'stock'], pass_context=True)
    async def stock(self, context):
        """Outputs current information on the Stock Market"""
        # TODO: Get important info to display
        # TODO: https://markets.money.cnn.com/services/api/chart/snapshot_chart_api.asp?symb=MSFT
        await context.send('To be added')

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='crypto', pass_context=True)
    async def crypto(self, context):
        """Outputs current information on Cryptocurrency"""
        conn = sqlite3.connect('./files/user_data.db')
        c = conn.cursor()

        base_url = 'https://coinmarketcap.com/currencies/'
        graph_url = 'https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/'
        thumb_url = 'https://chainz.cryptoid.info/logo/'
        alt_url = 'https://coinmarketcap.com/coins/'

        message = context.message.content.upper()
        args = message.split(" ")
        coin_name_url = '-'.join(args[1:3])

        try:
            c.execute('SELECT * FROM crypto_info WHERE coin_symbol=? LIMIT 1', [coin_name_url])
            row = c.fetchone()

            if row is None:         # if arg is coin full name
                pass
            else:                   # if arg = coin symbol
                coin_name_url = row[0]

            with urlopen("https://api.coinmarketcap.com/v1/ticker/{0}/".format(coin_name_url)) as coin_api:
                source = coin_api.read()
            coin_api = json.loads(source[1:-1])

            price_usd = float(coin_api['price_usd'])
            coin_id = coin_api['id']
            coin_name = coin_api['name']
            coin_rank = coin_api['rank']
            coin_symbol = coin_api['symbol']
            percent_change_1h = float(coin_api['percent_change_1h'])
            percent_change_24h = float(coin_api['percent_change_24h'])
            percent_change_7d = float(coin_api['percent_change_7d'])
            last_updated = int(coin_api['last_updated'])

            if price_usd > 1:
                price_usd = round(price_usd, 3)
            if price_usd > 5:
                price_usd = round(price_usd, 2)

            graph_emoji_1h, graph_emoji_24h, graph_emoji_7d = '📉', '📉', '📉'
            if percent_change_1h > 0:   # Life is just nested if statements
                graph_emoji_1h = '📈'
            if percent_change_24h > 0:
                graph_emoji_24h = '📈'
            if percent_change_7d > 0:
                graph_emoji_7d = '📈'

            seconds_ago = int(config.time.time()) - last_updated
            time_since_update = config.datetime.timedelta(seconds=seconds_ago)

            crypto_embed = discord.Embed(title='{} - {}'.format(coin_name, coin_symbol),
                                         url=base_url+coin_id, color=0x16e40c)
            crypto_embed.set_author(name='Crypto Tracker')
            crypto_embed.add_field(name='Current Price (in USD)', value='${}'.format(price_usd))
            crypto_embed.add_field(name='\u200b', value='\u200b')
            crypto_embed.add_field(name='Last Updated', value='{}'.format(time_since_update))
            crypto_embed.add_field(name='Last 1 Hour', value='{}% {}'.format(percent_change_1h, graph_emoji_1h))
            crypto_embed.add_field(name='Last 24 Hours', value='{}% {}'.format(percent_change_24h, graph_emoji_24h))
            crypto_embed.add_field(name='Last 7 Days', value='{}% {}'.format(percent_change_7d, graph_emoji_7d))
            crypto_embed.set_image(url=graph_url + coin_rank + '.png')
            crypto_embed.set_thumbnail(url=thumb_url + coin_symbol + '.png')
            crypto_embed.set_footer(text='Wrong information? Try \'!help crypto\' or go to {}'.format(base_url))
            await context.send(embed=crypto_embed)

        except urllib.error.HTTPError as err:
            await context.send('400 or 404')
        except Exception as err:
            await context.send('Unknown error')
        c.close()
        conn.close()


def setup(bot):
    bot.add_cog(Prices(bot))
