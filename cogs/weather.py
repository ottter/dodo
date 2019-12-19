from discord.ext import commands
import urllib.request
import urllib.error
import discord
import sqlite3
import config
import json
import sys

weather_description = """ ====  In-depth Weather Forecast Details  ====
                                .weather [id/name]           Tells you the weather of [location]
                                .forecast [id/name]          Tells you the forecast of [location]
                                .wset home [id/name]         Sets your home location
                                .wset unit [imperial/metric] Sets your preferred unit.
                                .wset [me/home]              Tells you your saved settings
                                Examples: .wset home london             
                                          .wset home Los Angeles, US
                                          .wset unit metric
                                          .weather home
                                          .forecast miami

                                Trouble finding your city? Try here: https://www.openweathermap.org/city/"""

base_url = 'https://www.openweathermap.org/city/'


def error_handler(user_city):
    error_embed = discord.Embed(title="Open Weather Map",
                                url='{}{}'.format(base_url, user_city),
                                color=0xff1717)
    error_embed.set_author(name='WeatherCog - Providing weather updates from OWM',
                           url='https://github.com/ottter/discord-bot',
                           icon_url='https://puu.sh/AIA3L/af06b7ffbe.png')
    error_embed.add_field(name="Non-existent location, or unable to find",
                          value="The link above will take you to what you tried searching for. ")
    index_error = error_embed.add_field(name="Missing search parameter",
                                        value="Try searching for a city: '.w london' or '.f atlanta'")
    error_embed.add_field(name="If you don't have a saved home:",
                          value="'.wset home [desired location]' to save your home",
                          inline=False)
    error_embed.set_footer(text="Try entering '.help weather' for further assistance.")

    return error_embed


def time_converter(weather_api_time):
    return config.datetime.datetime.fromtimestamp(int(weather_api_time)).strftime('%I:%M %p')


def weather_url_builder(service_param, search_param, city_id, input_unit):
    user_api_key = config.owm_token
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
    forecast = dict(
        id=raw_api_dict.get('city').get('id'),
        city=raw_api_dict.get('city').get('name'),
        country=raw_api_dict.get('city').get('country'),
        population=raw_api_dict.get('city').get('population'),

        # Due to nature of calls, they won't be exactly 3 hours away
        # Times (GMT): 12am (midnight), 3am, 6am, 9am, 12pm (noon), 3pm, 6pm, 9pm, 12am (midnight)
        h3_sky=raw_api_dict['list'][0]['weather'][0]['main'], h6_sky=raw_api_dict['list'][1]['weather'][0]['main'],
        h9_sky=raw_api_dict['list'][2]['weather'][0]['main'], h12_sky=raw_api_dict['list'][3]['weather'][0]['main'],
        h15_sky=raw_api_dict['list'][4]['weather'][0]['main'], h18_sky=raw_api_dict['list'][5]['weather'][0]['main'],
        h21_sky=raw_api_dict['list'][6]['weather'][0]['main'], h24_sky=raw_api_dict['list'][7]['weather'][0]['main'],
        h27_sky=raw_api_dict['list'][8]['weather'][0]['main'], h39_sky=raw_api_dict['list'][12]['weather'][0]['main'],
        h42_sky=raw_api_dict['list'][13]['weather'][0]['main'], h45_sky=raw_api_dict['list'][14]['weather'][0]['main'],
        h48_sky=raw_api_dict['list'][15]['weather'][0]['main'], h51_sky=raw_api_dict['list'][16]['weather'][0]['main'],
        h54_sky=raw_api_dict['list'][17]['weather'][0]['main'], h66_sky=raw_api_dict['list'][21]['weather'][0]['main'],
        h69_sky=raw_api_dict['list'][22]['weather'][0]['main'], h72_sky=raw_api_dict['list'][23]['weather'][0]['main'],
        h75_sky=raw_api_dict['list'][24]['weather'][0]['main'], h78_sky=raw_api_dict['list'][25]['weather'][0]['main'],

        h3_max=int(raw_api_dict['list'][0]['main']['temp_max']),
        h3_min=int(raw_api_dict['list'][0]['main']['temp_min']),
        h6_max=int(raw_api_dict['list'][1]['main']['temp_max']),
        h6_min=int(raw_api_dict['list'][1]['main']['temp_min']),
        h9_max=int(raw_api_dict['list'][2]['main']['temp_max']),
        h9_min=int(raw_api_dict['list'][2]['main']['temp_min']),
        h12_max=int(raw_api_dict['list'][3]['main']['temp_max']),
        h12_min=int(raw_api_dict['list'][3]['main']['temp_min']),
        h15_max=int(raw_api_dict['list'][4]['main']['temp_max']),
        h15_min=int(raw_api_dict['list'][4]['main']['temp_min']),
        h18_max=int(raw_api_dict['list'][5]['main']['temp_max']),
        h18_min=int(raw_api_dict['list'][5]['main']['temp_min']),
        h21_max=int(raw_api_dict['list'][6]['main']['temp_max']),
        h21_min=int(raw_api_dict['list'][6]['main']['temp_min']),
        h24_max=int(raw_api_dict['list'][7]['main']['temp_max']),
        h24_min=int(raw_api_dict['list'][7]['main']['temp_min']),
        h27_max=int(raw_api_dict['list'][8]['main']['temp_max']),
        h27_min=int(raw_api_dict['list'][8]['main']['temp_min']),

        h42_max=int(raw_api_dict['list'][13]['main']['temp_max']),
        h42_min=int(raw_api_dict['list'][13]['main']['temp_min']),
        h45_max=int(raw_api_dict['list'][14]['main']['temp_max']),
        h45_min=int(raw_api_dict['list'][14]['main']['temp_min']),
        h48_max=int(raw_api_dict['list'][15]['main']['temp_max']),
        h48_min=int(raw_api_dict['list'][15]['main']['temp_min']),
        h51_max=int(raw_api_dict['list'][16]['main']['temp_max']),
        h51_min=int(raw_api_dict['list'][16]['main']['temp_min']),
        h54_max=int(raw_api_dict['list'][17]['main']['temp_max']),
        h54_min=int(raw_api_dict['list'][17]['main']['temp_min']),

        h66_max=int(raw_api_dict['list'][21]['main']['temp_max']),
        h66_min=int(raw_api_dict['list'][21]['main']['temp_min']),
        h69_max=int(raw_api_dict['list'][22]['main']['temp_max']),
        h69_min=int(raw_api_dict['list'][22]['main']['temp_min']),
        h72_max=int(raw_api_dict['list'][23]['main']['temp_max']),
        h72_min=int(raw_api_dict['list'][23]['main']['temp_min']),
        h75_max=int(raw_api_dict['list'][24]['main']['temp_max']),
        h75_min=int(raw_api_dict['list'][24]['main']['temp_min']),
        h78_max=int(raw_api_dict['list'][25]['main']['temp_max']),
        h78_min=int(raw_api_dict['list'][25]['main']['temp_min']),
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

    if int(weather['wind_deg']) in range(337, 361):
        weather['direction'] = 'North'
    elif int(weather['wind_deg']) in range(0, 22):
        weather['direction'] = 'North'
    elif int(weather['wind_deg']) in range(22, 67):
        weather['direction'] = 'NE'
    elif int(weather['wind_deg']) in range(67, 112):
        weather['direction'] = 'East'
    elif int(weather['wind_deg']) in range(112, 157):
        weather['direction'] = 'SE'
    elif int(weather['wind_deg']) in range(157, 202):
        weather['direction'] = 'South'
    elif int(weather['wind_deg']) in range(202, 247):
        weather['direction'] = 'SW'
    elif int(weather['wind_deg']) in range(247, 292):
        weather['direction'] = 'West'
    elif int(weather['wind_deg']) in range(292, 337):
        weather['direction'] = 'NW'
    elif int(weather['wind_deg']) in range(292, 337):
        weather['direction'] = 'NW'
    elif int(weather['wind_deg']) == -1:
        weather['direction'] = '\u200b'
    return weather


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)  # _ use per _ seconds per user/channel/server #
    @commands.command(name='weather',
                      description=weather_description,
                      brief='Provides updated weather information',
                      aliases=['temp', 'w'],
                      pass_context=True)
    async def weather_api(self, context):
        message = context.message.content
        user_input = message.split(' ', 1)

        icon_url = 'http://openweathermap.org/img/w/'
        wind_sign = 'km/h'
        sky_deets = 'clear'  # sometimes the API doesn't have an entry and it makes code act weird
        temp_sign = 'C'
        user_city = 'fucking'  # haven't thought of a better way to implement backup defaults

        try:
            user_city = str(user_input[1])

            conn = sqlite3.connect('user_data.db')
            c = conn.cursor()
            user = context.message.author.id
            c.execute('SELECT * FROM weather_home WHERE discord_id=?', [user])

            if user_city == 'home':
                for row in c.fetchall():
                    weather = weather_data(weather_fetch(weather_url_builder('weather?', 'id=', row[1], row[2])))
                    c.execute('SELECT s.sky_text FROM sky_condition s INNER JOIN weather_home w '
                              'WHERE s.sky_id=? AND w.discord_id=?', [weather['sky_id'], user])
                    sky_deets = c.fetchone()

                    data_url = base_url + str(row[1])

                    if row[2] == 'imperial':
                        temp_sign = 'F'
                        wind_sign = 'mph'
                        wind_con = str(round(weather['wind'], 1))
                    else:
                        wind_con = str(round(weather['wind'] * 3.6, 1))

            else:
                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'q=', user_city, 'metric')))

                c.execute('SELECT sky_text FROM sky_condition WHERE sky_id=?', [weather['sky_id']])
                sky_deets = c.fetchone()

                data_url = base_url + str(weather['id'])
                wind_con = str(round(weather['wind'] * 3.6, 1))


            map_url = 'https://www.google.com/maps/@{},{},12z'.format(weather['latitude'], weather['longitude'])

            seconds_ago = int(config.time.time()) - weather['epoch_update']
            time_ago = config.datetime.timedelta(seconds=seconds_ago)

            data_icon = icon_url + str(weather['icon']) + '.png'

            weather_embed = discord.Embed(title='{}, {} - {} :flag_{}:'
                                          .format(weather['city'], weather['country'], weather['id'],
                                                  weather['country'].lower()),
                                          url=data_url, description='Right now it is {}°{} {}'
                                          .format(weather['temp'], temp_sign, sky_deets[0]), color=0x16e40c)
            weather_embed.set_thumbnail(url=f'{data_icon}')
            weather_embed.set_author(name='WeatherCog - Providing weather updates from OWM',
                                     url='https://github.com/ottter/discord-bot',
                                     icon_url='https://puu.sh/AIA3L/af06b7ffbe.png')
            weather_embed.add_field(name='Current Temp', value='{}°{}'.format(weather['temp'], temp_sign))
            weather_embed.add_field(name='High & Low Temp',
                                    value='{}° / {}°'.format(weather['temp_max'], weather['temp_min']))
            weather_embed.add_field(name='Humidity', value='{}%'.format(weather['humidity']))
            weather_embed.add_field(name='Wind', value='{} {} {} ({}°)'
                                    .format(wind_con, wind_sign, weather['direction'], weather['wind_deg']))
            weather_embed.add_field(name='Lat & Long',
                                    value='[{}, {}]({})'.format(weather['latitude'], weather['longitude'], map_url))
            weather_embed.add_field(name='Time Since Last Update', value='{}'.format(time_ago))
            weather_embed.set_footer(text=f'Wrong information? Try \'.help weather\' or go to {base_url}')
            await context.send(embed=weather_embed)

        except urllib.error.HTTPError as err:
            print(err)
            await context.send(embed=error_handler(user_city))
        except IndexError as err:
            print(err)
            await context.send(embed=error_handler(user_city))
        except (TypeError, KeyError, Exception) as err:
            print(err)
            await context.send(embed=error_handler(user_city))

    @commands.cooldown(1, 3, commands.BucketType.user)  # _ use per _ seconds per user/channel/server #
    @commands.command(name='forecast',
                      description=weather_description,
                      brief='Provides updated weather information',
                      aliases=['fcast', 'f'],
                      pass_context=True)
    async def forecast_api(self, context):

        message = context.message.content
        user_input = message.split(' ', 1)

        icon_url = 'http://openweathermap.org/img/w/'
        sky_deets = 'clear'
        temp_sign = 'C'
        user_city = 'fucking'  # haven't thought of a better way to implement backup defaults

        try:
            conn = sqlite3.connect('user_data.db')
            c = conn.cursor()
            user = context.message.author.id
            c.execute('SELECT * FROM weather_home WHERE discord_id=?', [user])

            user_city = str(user_input[1])

            if user_city == 'home':
                for row in c.fetchall():
                    weather = weather_data(weather_fetch(weather_url_builder('weather?', 'id=', row[1], row[2])))
                    forecast = forecast_data(weather_fetch(weather_url_builder('forecast?', 'id=', row[1], row[2])))
                    c.execute('SELECT s.sky_text FROM sky_condition s INNER JOIN weather_home w '
                              'WHERE s.sky_id=? AND w.discord_id=?', [weather['sky_id'], user])
                    sky_deets = c.fetchone()
                    data_url = base_url + str(row[1])

                    if row[2] == 'imperial':
                        temp_sign = 'F'


            else:
                forecast = forecast_data(weather_fetch(weather_url_builder('forecast?', 'q=', user_city, 'metric')))
                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'q=', user_city, 'metric')))

                c.execute('SELECT sky_text FROM sky_condition WHERE sky_id=?', [weather['sky_id']])
                sky_deets = c.fetchone()
                data_url = base_url + str(weather['id'])


            map_url = 'https://www.google.com/maps/@{},{},12z'.format(weather['latitude'], weather['longitude'])
            data_icon = icon_url + str(weather['icon']) + '.png'

            temp_max_6 = max(weather['temp_max'], forecast['h3_max'],
                             forecast['h6_max'], forecast['h9_max'])
            temp_min_6 = min(weather['temp_min'], forecast['h3_min'],
                             forecast['h6_min'], forecast['h9_min'])
            temp_max_24 = max(forecast['h15_max'], forecast['h18_max'], forecast['h21_max'],
                              forecast['h24_max'], forecast['h27_max'])
            temp_min_24 = min(forecast['h15_min'], forecast['h18_min'], forecast['h21_min'],
                              forecast['h24_min'], forecast['h27_min'])
            temp_max_48 = max(forecast['h42_max'], forecast['h45_max'], forecast['h48_max'],
                              forecast['h51_max'], forecast['h54_max'])
            temp_min_48 = min(forecast['h42_min'], forecast['h45_min'], forecast['h48_min'],
                              forecast['h51_min'], forecast['h54_min'])
            temp_max_72 = max(forecast['h66_max'], forecast['h69_max'], forecast['h72_max'],
                              forecast['h75_max'], forecast['h78_max'])
            temp_min_72 = min(forecast['h66_min'], forecast['h69_min'], forecast['h72_min'],
                              forecast['h75_min'], forecast['h78_min'])

            sky_6_string = (weather['sky'], forecast['h3_sky'], forecast['h6_sky'], forecast['h9_sky'])
            sky_6_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_6_string]
            sky_6_filter = " | ".join(set(sky_6_filter))

            sky_24_string = (forecast['h18_sky'], forecast['h21_sky'], forecast['h24_sky'], forecast['h27_sky'])
            sky_24_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_24_string]
            sky_24_filter = " | ".join(set(sky_24_filter))

            sky_48_string = (forecast['h45_sky'], forecast['h48_sky'], forecast['h51_sky'], forecast['h54_sky'])
            sky_48_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_48_string]
            sky_48_filter = " | ".join(set(sky_48_filter))

            sky_72_string = (forecast['h69_sky'], forecast['h72_sky'], forecast['h75_sky'], forecast['h78_sky'])
            sky_72_filter = [s.replace('Thunderstorm', 'Storms') for s in sky_72_string]
            sky_72_filter = " | ".join(set(sky_72_filter))

            forecast_embed = discord.Embed(title='{}, {} - {} :flag_{}:'
                                           .format(weather['city'], weather['country'], weather['id'],
                                                   weather['country'].lower()),
                                           url=data_url, description='Right now it is {}°{} {}.\nWhat you can'
                                                                     ' expect to see over the next few days:'
                                           .format(weather['temp'], temp_sign, sky_deets[0]), color=0x16e40c)
            forecast_embed.set_thumbnail(url=f'{data_icon}')
            forecast_embed.set_author(name='WeatherCog - Providing forecast updates from OWM',
                                      url='https://github.com/ottter/discord-bot',
                                      icon_url='https://puu.sh/AIA3L/af06b7ffbe.png')
            forecast_embed.add_field(name='Over the next few hours',
                                     value=f'{temp_min_6}-{temp_max_6}°{temp_sign}\n{sky_6_filter}')
            forecast_embed.add_field(name='Tomorrow',
                                     value=f'{temp_min_24}-{temp_max_24}°{temp_sign}\n{sky_24_filter}')
            forecast_embed.add_field(name='In two days',
                                     value=f'{temp_min_48}-{temp_max_48}°{temp_sign}\n{sky_48_filter}')
            forecast_embed.add_field(name='Three days from now',
                                     value=f'{temp_min_72}-{temp_max_72}°{temp_sign}\n{sky_72_filter}')
            forecast_embed.set_footer(text=f'Wrong information? Try \'.help weather\' or go to {base_url}')
            await context.send(embed=forecast_embed)

        except urllib.error.HTTPError as err:
            await context.send(embed=error_handler(user_city))

        except IndexError as err:
            await context.send(embed=error_handler(user_city))

        except (TypeError, KeyError, Exception) as err:
            await context.send(embed=error_handler(user_city))

    @commands.cooldown(1, 1, commands.BucketType.user)  # _ use per _ seconds per user/channel/server #
    @commands.command(name='wset',
                      description='Settings for WeatherBot. ".help weather" for assistance',
                      brief='Set user\'s saved weather information',
                      aliases=['fpset', 'weatherset'],
                      pass_context=True)
    async def weather_settings(self, context):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        user = context.message.author.id
        message = context.message.content
        args = message.split(" ", 1)

        if args[1] == 'home':
            home_set = args[2]

            if home_set in range(1, 9999999):
                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'id=', home_set, 'metric')))
                c.execute('INSERT OR IGNORE INTO weather_home (discord_id) VALUES(?)', (user,))
                c.execute('UPDATE weather_home SET home_loc=? WHERE discord_id=?', (home_set, user))
                for row in c.fetchall():
                    if row[2] is None:
                        unit = 'metric'
                    else:
                        unit = row[2]
                    c.execute('UPDATE weather_home SET unit=? WHERE discord_id=?', (unit, user))

            else:
                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'q=', home_set, 'metric')))
                c.execute('INSERT OR IGNORE INTO weather_home (discord_id) VALUES(?)', (user,))
                c.execute('UPDATE weather_home SET home_loc=? WHERE discord_id=?', (weather['id'], user))
                for row in c.fetchall():
                    if row[2] is None:
                        unit = 'metric'
                    else:
                        unit = row[2]
                    c.execute('UPDATE weather_home SET unit=? WHERE discord_id=?', (unit, user))

            await context.send('```Success! You set your home location to: {}, {}\n'
                                  'Not what you\'re looking for? Try \'!help weather\' or go here: {}```'
                                  .format(weather['city'], weather['country'], base_url))

        elif args[1] == 'unit':
            u = str(''.lower().join(args[2]))
            if (u == 'metric') or (u == 'c') or (u == 'celsius') or (u == 'met'):
                c.execute('INSERT OR IGNORE INTO weather_home (discord_id) VALUES(?)', (user,))
                c.execute('UPDATE weather_home SET unit=? WHERE discord_id=?', ('metric', user))
                await context.send('```Success! You set your preferred unit to: Metric```')

            elif (u == 'imperial') or (u == 'f') or (u == 'fahrenheit') or (u == 'imp'):
                c.execute('INSERT OR IGNORE INTO weather_home (discord_id) VALUES(?)', (user,))
                c.execute('UPDATE weather_home SET unit=? WHERE discord_id=?', ('imperial', user))
                await context.send('```Success! You set your preferred unit to: Imperial```')

            else:
                await context.send('```Typo... I think. Try again.```')

        elif (args[1] == 'me') or (args[1] == 'settings'):
            c.execute('SELECT * FROM weather_home WHERE discord_id=?', [user])
            for row in c.fetchall():
                weather = weather_data(weather_fetch(weather_url_builder('weather?', 'id=', row[1], row[2])))
                await context.send('``` Your home location is:  {}, {} - {}\n Your preferred unit is: {}```'
                                      .format(weather['city'], weather['country'], row[1], row[2]))

        else:
            await context.send('``` Acceptable Formats: .wset home [city name/city id] \n '
                                  '                    .wset unit [f/c/imperial/metric/fahrenheit/celsius```')

        conn.commit()
        c.close()
        conn.close()


def setup(bot):
    bot.add_cog(Weather(bot))