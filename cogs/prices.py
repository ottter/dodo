from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
from discord.ext import commands
import config
import json

def create_coin_dict(data, coin_symbol, fiat_currency):
    coin_stats = data[coin_symbol]['quote'][fiat_currency]

    data_dict = dict()
    data_dict['coin_name'] = data[coin_symbol]['name']
    data_dict['coin_symbol'] = data[coin_symbol]['symbol']
    data_dict['current_price'] = coin_stats['price']
    data_dict['percent_change_1h'] = coin_stats['percent_change_1h']
    data_dict['percent_change_24h'] = coin_stats['percent_change_24h']
    data_dict['percent_change_7d'] = coin_stats['percent_change_7d']
    data_dict['last_updated'] = coin_stats['last_updated']
    return data_dict

def coin_output(data, args):
    coin_symbol = args[1]
    fiat_currency = 'USD'   #TODO: Accept other currency
    data_dict = create_coin_dict(data, coin_symbol, fiat_currency)

    # TODO: make below more pythonic
    if data_dict['current_price'] > 1:
        data_dict['current_price'] = round(data_dict['current_price'], 3)
    if data_dict['current_price'] > 5:
        data_dict['current_price'] = round(data_dict['current_price'], 2)

    data_dict['graph_emoji'] = []
    for x in [data_dict['percent_change_1h'], data_dict['percent_change_24h'], data_dict['percent_change_7d']]:
        if x >= 0:
            data_dict['graph_emoji'].append('📈')
        else:
            data_dict['graph_emoji'].append('📉')

    print(data_dict)
    return #should return the embed


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
    @commands.command(name='coins', pass_context=True)
    async def coin(self, context):
        """Outputs current information on Cryptocurrency"""

        args = context.message.content.upper().split(" ")

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'symbol': args[1]
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.COINMARKET_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return await coin_output(data['data'], args)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


def setup(bot):
    bot.add_cog(Prices(bot))
