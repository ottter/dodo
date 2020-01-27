from discord.ext import commands
import urllib.request
import urllib.error
import discord
import config
import json

# I wrote this like 2 years ago. Don't judge me

weather_description = """ ====  In-depth Weather Forecast Details  ====
                                Trouble finding your city? Try here: https://www.openweathermap.org/city/"""

base_url = 'https://www.openweathermap.org/city/'


def time_converter(weather_api_time):
    return config.datetime.datetime.fromtimestamp(int(weather_api_time)).strftime('%I:%M %p')


def weather_url_builder(service_param, search_param, city_id, input_unit):
    user_api_key = config.OWM_TOKEN
    api_url = 'http://api.openweathermap.org/data/2.5/'  # 4207400
    weather_api_url = '{}{}{}{}&mode=json&units={}&APPID={}' \
        .format(api_url, service_param, search_param, city_id, input_unit, user_api_key)
    return weather_api_url


def weather_fetch(full_api_url):
    with urllib.request.urlopen(full_api_url) as url:
        output = url.read().decode('utf-8')
        raw_api_dict = json.loads(output)
    return raw_api_dict


def forecast_data(raw_api_dict):
    # OWM API creates the forecast in 3 hour intervals, so [0]= 3 hours from present, [1]= 6 hours, up to 78 hours
    # Each of the following lists works like this for their respective value
    hourly_sky, hourly_max, hourly_min = ([] for i in range(3))
    for x in range(26):
        hourly_sky.append(raw_api_dict['list'][x]['weather'][0]['main'])
        hourly_min.append(raw_api_dict['list'][x]['main']['temp_min'])
        hourly_max.append(raw_api_dict['list'][x]['main']['temp_max'])

    forecast = dict(
        id=raw_api_dict.get('city').get('id'),
        city=raw_api_dict.get('city').get('name'),
        country=raw_api_dict.get('city').get('country'),
        population=raw_api_dict.get('city').get('population'),

        sky_hourly = hourly_sky,
        temp_max = hourly_max,
        temp_min = hourly_min,
    )
    return forecast


def weather_data(raw_api_dict):
    weather = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        id=raw_api_dict.get('id'),
        icon=raw_api_dict['weather'][0]['icon'],
        longitude=raw_api_dict.get('coord').get('lon'),
        latitude=raw_api_dict.get('coord').get('lat'),
        temp=int(raw_api_dict.get('main').get('temp')),
        temp_max=int(raw_api_dict.get('main').get('temp_max')),
        temp_min=int(raw_api_dict.get('main').get('temp_min')),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sky_id=raw_api_dict['weather'][0]['id'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=int(raw_api_dict.get('wind').get('deg', -1)),
        dt=time_converter(raw_api_dict.get('dt')),
        epoch_update=raw_api_dict.get('dt'),
        cloudiness=raw_api_dict.get('clouds').get('all'),
        direction='Undefined',
        sky_detail='Undefined'
    )

    wind_direction = {range(337, 361): 'N', range(0, 22): 'N', range(22, 67): 'NE', range(67, 112): 'E',
                      range(112, 157): 'SE', range(157, 202): 'S', range(202, 247): 'SW', range(247, 292): 'W',
                      range(292, 337): 'NW', range(-1,0): '\u200b'}

    for k in wind_direction:
        if weather['wind_deg'] in k:
            weather['direction'] = wind_direction[k]

    return weather


class Weather(commands.Cog):
    """Weather and Forecast updates"""
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)  # _ use per _ seconds per user/channel/server #
    @commands.command(name='weather',
                      description=weather_description,
                      brief='Provides updated weather information',
                      aliases=['temp', 'w'],
                      pass_context=True)
    async def weather_api(self, context):
        """See the current weather for a given location
        How to view: .weather [city]"""

        message = context.message.content
        user_input = message.split(' ', 1)

        icon_url = 'http://openweathermap.org/img/w/'
        wind_sign = 'km/h'
        condition = 'clear'  # sometimes the API doesn't have an entry and it makes code act weird
        temp_sign = 'C'
        user_city = 'atlanta'  # haven't thought of a better way to implement backup defaults

        collection = config.db['weather_home']
        conditions = config.db['sky_condition']

        try:
            user_city = str(user_input[1].replace(' ', '%20'))
            user = context.message.author.id

            if user_city == 'home':

                results = collection.find({'_id': user})
                row = []
                for result in results:
                    row = [result['_id'], result['home_loc'], result['unit']]

                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'id=', row[1], row[2])))

                data_url = base_url + str(row[1])

                if row[2] == 'imperial':
                    temp_sign = 'F'
                    wind_sign = 'mph'
                    wind_con = str(round(weather['wind'], 1))
                else:
                    wind_con = str(round(weather['wind'] * 3.6, 1))

            else:
                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'q=', user_city, 'metric')))

                data_url = base_url + str(weather['id'])
                wind_con = str(round(weather['wind'] * 3.6, 1))

            map_url = 'https://www.google.com/maps/@{},{},12z'.format(weather['latitude'], weather['longitude'])

            seconds_ago = int(config.time.time()) - weather['epoch_update']
            time_ago = config.datetime.timedelta(seconds=seconds_ago)

            data_icon = icon_url + str(weather['icon']) + '.png'

            sky_detail = conditions.find({'sky_id': f'{weather["sky_id"]}'})
            for condition in sky_detail:
                condition = condition['sky_text']

            weather_embed = discord.Embed(title=f"{weather['city']}, {weather['country']} - "
                                                f"{weather['id']} :flag_{weather['country'].lower()}:",
                                          url=data_url,
                                          description=f"Right now it is {weather['temp']}°{temp_sign} and {condition}",
                                          color=0x16e40c)
            weather_embed.set_thumbnail(url=f'{data_icon}')
            weather_embed.set_author(name='WeatherCog - Providing weather updates from OWM',
                                     url='https://github.com/ottter/discord-bot',
                                     icon_url='https://puu.sh/AIA3L/af06b7ffbe.png')
            weather_embed.add_field(name='Current Temp',
                                    value=f"{weather['temp']}°{temp_sign}")
            weather_embed.add_field(name='High & Low Temp',
                                    value=f"{weather['temp_max']}° / {weather['temp_min']}°")
            weather_embed.add_field(name='Humidity',
                                    value=f"{weather['humidity']}%")
            weather_embed.add_field(name='Wind',
                                    value=f"{weather['direction']} {wind_con}{wind_sign}")
            weather_embed.add_field(name='Lat & Long',
                                    value=f"[{weather['latitude']}, {weather['longitude']}]({map_url})")
            weather_embed.add_field(name='Last Updated',
                                    value=f'{time_ago}')
            weather_embed.set_footer(text=f'Wrong information? Try \'.help Weather\' or go to {base_url}')
            await context.send(embed=weather_embed)

        except urllib.error.HTTPError as err:
            print(err)
            await context.send('')
        except IndexError as err:
            print(err)
            await context.send('')
        except Exception as err:
            print(err)
            await context.send('')

    @commands.cooldown(1, 3, commands.BucketType.user)  # _ use per _ seconds per user/channel/server #
    @commands.command(name='forecast',
                      description=weather_description,
                      brief='Provides updated weather information',
                      aliases=['fcast', 'f'],
                      pass_context=True)
    async def forecast_api(self, context):
        """See the future forecast for a given location
        How to view: .forecast [city]"""

        message = context.message.content
        user_input = message.split(' ', 1)

        icon_url = 'http://openweathermap.org/img/w/'
        condition = 'clear'
        temp_sign = 'C'
        user_city = 'atlanta'  # haven't thought of a better way to implement backup defaults

        collection = config.db['weather_home']
        conditions = config.db['sky_condition']

        try:
            user_city = str(user_input[1].replace(' ', '%20'))
            user = context.message.author.id

            if user_city == 'home':
                results = collection.find({'_id': user})
                row = []
                for result in results:
                    row = [result['_id'], result['home_loc'], result['unit']]

                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'id=', row[1], row[2])))
                forecast = forecast_data(weather_fetch(weather_url_builder('forecast?', 'id=', row[1], row[2])))
                data_url = base_url + str(row[1])

                sky_detail = conditions.find({'sky_id': f'{weather["sky_id"]}'})
                for condition in sky_detail:
                    condition = condition['sky_text']

                if row[2] == 'imperial':
                    temp_sign = 'F'

            else:
                forecast = forecast_data(weather_fetch(weather_url_builder('forecast?', 'q=', user_city, 'metric')))
                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'q=', user_city, 'metric')))

                sky_detail = conditions.find({'sky_id': f'{weather["sky_id"]}'})
                for condition in sky_detail:
                    condition = condition['sky_text']

                data_url = base_url + str(weather['id'])

            map_url = 'https://www.google.com/maps/@{},{},12z'.format(weather['latitude'], weather['longitude'])
            data_icon = icon_url + str(weather['icon']) + '.png'

            temp_max_6 = int(max(forecast['temp_max'][0:3]))
            temp_min_6 = int(min(forecast['temp_min'][0:3]))

            temp_max_24 = int(max(forecast['temp_max'][4:9]))
            temp_min_24 = int(min(forecast['temp_min'][4:9]))

            temp_max_48 = int(max(forecast['temp_max'][13:18]))
            temp_min_48 = int(min(forecast['temp_min'][13:18]))

            temp_max_72 = int(max(forecast['temp_max'][21:26]))
            temp_min_72 = int(min(forecast['temp_min'][21:26]))

            sky_6_string = (forecast['sky_hourly'][0:3])
            sky_6_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_6_string]
            sky_6_filter = " | ".join(set(sky_6_filter))

            sky_24_string = (forecast['sky_hourly'][5:9])
            sky_24_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_24_string]
            sky_24_filter = " | ".join(set(sky_24_filter))

            sky_48_string = (forecast['sky_hourly'][14:18])
            sky_48_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_48_string]
            sky_48_filter = " | ".join(set(sky_48_filter))

            sky_72_string = (forecast['sky_hourly'][22:26])
            sky_72_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_72_string]
            sky_72_filter = " | ".join(set(sky_72_filter))

            forecast_embed = discord.Embed(title='{}, {} - {} :flag_{}:'
                                           .format(weather['city'], weather['country'], weather['id'],
                                                   weather['country'].lower()),
                                           url=data_url, description='Right now it is {}°{} and {}.\n'
                                                                     'What you can expect to see:'
                                           .format(weather['temp'], temp_sign, condition), color=0x16e40c)
            forecast_embed.set_thumbnail(url=f'{data_icon}')
            forecast_embed.set_author(name='WeatherCog - Providing forecast updates from OWM',
                                      url='https://github.com/ottter/discord-bot',
                                      icon_url='https://puu.sh/AIA3L/af06b7ffbe.png')
            forecast_embed.add_field(name='Next few hours',
                                     value=f'{temp_min_6} / {temp_max_6}°{temp_sign}\n{sky_6_filter}')
            forecast_embed.add_field(name='Tomorrow',
                                     value=f'{temp_min_24} / {temp_max_24}°{temp_sign}\n{sky_24_filter}')
            forecast_embed.add_field(name='Next few days',
                                     value=f'{temp_min_48} / {temp_max_48}°{temp_sign}\n{sky_48_filter}')
            forecast_embed.add_field(name='and beyond',
                                     value=f'{temp_min_72} / {temp_max_72}°{temp_sign}\n{sky_72_filter}')
            forecast_embed.set_footer(text=f'Wrong information? Try \'.help Weather\' or go to {base_url}')
            await context.send(embed=forecast_embed)

        except urllib.error.HTTPError as err:
            await context.send('')

        except IndexError as err:
            await context.send('')

        except Exception as err:
            await context.send('')

    @commands.cooldown(1, 1, commands.BucketType.user)  # _ use per _ seconds per user/channel/server #
    @commands.command(name='wset',
                      description='Settings for WeatherBot. ".help Weather" for assistance',
                      brief='Set user\'s saved weather information',
                      aliases=['fset', 'weatherset'],
                      pass_context=True)
    async def weather_settings(self, context):
        """Assign settings for .weather and .forecast
        Set home location: .wset home [city]
        Set preferred unit: .wset unit [c/f]
        View saved settings: .wset [me/home]"""

        collection = config.db['weather_home']

        user = context.message.author.id
        args = context.message.content.lower().split(" ", 2)

        if args[1] == 'home':
            weather = weather_data(weather_fetch(weather_url_builder('weather?', 'q=', args[2], 'metric')))

            collection.update_one({'_id': user}, {'$set': {'home_loc': weather['id'], 'unit': 'metric'}},
                                  upsert=True)

            await context.send(f"Success! You set your preferred unit to: `{weather['city']}, {weather['country']}`\n"
                               f"Not what you're looking for? Try \'!help Weather\' or go here: {base_url}")

        elif args[1] == 'unit':
            unit = {'c': 'metric', 'f': 'imperial'}

            if args[2] in unit.keys():
                collection.update_one({'_id': user}, {'$set': {'unit': unit[args[2]]}}, upsert=True)
                await context.send(f"Success! You set your preferred unit to: `{unit[args[2]]}`")

            else:
                await context.send('Accepted Inputs:`C` for Celsius or `F` for Fahrenheit')

        else:
            await context.send('Accepted Inputs: `.wset home [city name/city id]` and `.wset unit [F/C]`')

def setup(bot):
    bot.add_cog(Weather(bot))