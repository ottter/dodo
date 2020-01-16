from discord.ext import commands
from urllib.request import urlopen
import urllib.error
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

        base_url = 'https://coinmarketcap.com/currencies/'
        graph_url = 'https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/'
        thumb_url = 'https://chainz.cryptoid.info/logo/'
        # alt_url = 'https://coinmarketcap.com/coins/'

        args = context.message.content.upper().split(" ")
        coin_name_url = '-'.join(args[1:3])

        collection = config.db['cryptocurrency']

        try:
            results = collection.find({'coin_symbol': coin_name_url})
            row = []
            for result in results:
                row = [result['coin_name'], result['coin_symbol']]

            if not row:         # if arg = coin full name
                pass
            else:               # if arg = coin symbol
                coin_name_url = row[0]

            with urlopen(f"https://api.coinmarketcap.com/v1/ticker/{coin_name_url}/") as coin_api:
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

            graph_emoji = []
            for x in [percent_change_1h, percent_change_24h, percent_change_7d]:
                if x >= 0:
                    graph_emoji.append('📈')
                else:
                    graph_emoji.append('📉')

            seconds_ago = int(config.time.time()) - last_updated
            time_since_update = config.datetime.timedelta(seconds=seconds_ago)

            crypto_embed = discord.Embed(title=f'{coin_name} - {coin_symbol}', url=base_url+coin_id, color=0x16e40c)
            crypto_embed.set_author(name='Crypto Tracker')
            crypto_embed.add_field(name='Current Price (in USD)', value=f'${price_usd}')
            crypto_embed.add_field(name='\u200b', value='\u200b')
            crypto_embed.add_field(name='Last Updated', value=f'{time_since_update}')
            crypto_embed.add_field(name='Last 1 Hour', value=f'{percent_change_1h}% {graph_emoji[0]}')
            crypto_embed.add_field(name='Last 24 Hours', value=f'{percent_change_24h}% {graph_emoji[1]}')
            crypto_embed.add_field(name='Last 7 Days', value=f'{percent_change_7d}% {graph_emoji[2]}')
            crypto_embed.set_image(url=graph_url + coin_rank + '.png')
            crypto_embed.set_thumbnail(url=thumb_url + coin_symbol + '.png')
            crypto_embed.set_footer(text=f"Wrong information? Try '!help crypto' or go to {base_url}")
            await context.send(embed=crypto_embed)

        except urllib.error.HTTPError:
            await context.send('400 or 404 Error')
        except Exception as err:
            print(f'crypto: Error: {err}\t Input: {args}')
            await context.send('Unknown error')

def setup(bot):
    bot.add_cog(Prices(bot))
