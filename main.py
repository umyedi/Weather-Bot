from ressources import AuthTweepy, AuthPyown, currentTime, CUR_DIR
import pyowm
import tweepy
import time
import logging
import sys
import re

logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.FileHandler(filename='main.log', mode='a', encoding='UTF-8'),
                        logging.StreamHandler(sys.stdout),
                    ],
                    format='[%(asctime)s] %(levelname)s -> %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger()

def allWeatherInfos(city):
    """Gets information about the weather in a city.

    Args:
        city (str): name of a city

    Returns:
        list: contain :  city's name, current date and hour, weather, temperature, temperature feeling and wind speed
    """
    try:
        owm = AuthPyown()
        mgr = owm.weather_manager()

        location = mgr.weather_at_place(city)
        date = currentTime("%d/%m/%Y")
        hour = currentTime("%Hh%M")
        weather = location.weather.detailed_status
        temp = location.weather.temperature('celsius')
        wind_speed = location.weather.wind().get('speed', 0)
        wind_speed = round(wind_speed*3.6, 2)
        return [city, date, hour, weather, int(round(temp['temp'])), int(round(temp['feels_like'])), wind_speed]

    except pyowm.commons.exceptions.NotFoundError as e:
        logger.warning(f"The location for '{city}' isn't valid ({e}).")
        return False
    except pyowm.commons.exceptions.APIRequestError as e:
        logger.warning(f"Please enter a city name ({e}).")
        return False
    except pyowm.commons.exceptions.InvalidSSLCertificateError as e:
        logger.warning(f"An external program blocks the connections ({e}).")
        return False
    except pyowm.commons.exceptions.UnauthorizedError as e:
        logger.warning(f"Incorrect Pyowm authentication key ({e}).")
        return False


def updateProfilePicture(weather):
    """Updates the profile picture of the bot according to the weather.

    Args:
        weather (str): city weather

    Returns:
        bool: True if the function succed, False if an error occured
    """
    DIRECTORY = CUR_DIR + '\\profile_pictures\\'

    if weather == 'ciel dégagé':
        AuthTweepy().update_profile_image(f'{DIRECTORY}sunny.png')
    elif weather in ['couvert', 'peu nuageux', 'partiellement nuageux']:
        AuthTweepy().update_profile_image(f'{DIRECTORY}overcast.png')
    elif weather == 'nuageux':
        AuthTweepy().update_profile_image(f'{DIRECTORY}cloudy.png')
    elif weather == 'pluie modérée':
        AuthTweepy().update_profile_image(f'{DIRECTORY}rainy.png')
    elif weather == 'légère pluie':
        AuthTweepy().update_profile_image(f'{DIRECTORY}slightly_rainy.png')
    elif weather in ['brume', 'brouillard']:
        AuthTweepy().update_profile_image(f'{DIRECTORY}mist.png')
    elif weather == 'orageux':
        AuthTweepy().update_profile_image(f'{DIRECTORY}stormy.png')
    elif weather == 'légères chutes de neige':
        AuthTweepy().update_profile_image(f'{DIRECTORY}snowy.png')
    else:
        logger.error(f"No profile pictures match '{weather}' for now.")
        return False

    return True

def publishTweet(weather_infos):
    """Publishes a Tweet based on information about a city.

    Args:
        weather_infos (list): the list that the allWeatherInfos function returns

    Returns:
        str: the Tweet published
    """

    tweet = f"""
    Voici la météo pour {weather_infos[0]}, le {weather_infos[1]} à {weather_infos[2]}:
        ☀️ Temps : {weather_infos[3]}
        🌡️ Température : {weather_infos[4]}°C (ressenti {weather_infos[5]}°C)
        💨 Vitesse du vent : {weather_infos[6]} km/h"""

    try:
        AuthTweepy().update_status(tweet)
        logger.info("Tweet published !")
        return tweet

    except tweepy.errors.Forbidden as e:
        logger.warning(f"The Tweet you are trying to post already exists ({e}).")

    except tweepy.errors.Unauthorized as e:
        logger.warning(f"Incorrect Tweepy authentication keys ({e}).")

def manualRun(city):
    """Publishes a Tweet based on information about a city and updates the profile picture accordingly.

    Args:
        city (str): name of a city

    Returns:
        bool: True if there isn't any error, else False
    """
    infos = allWeatherInfos(city)
    publish = publishTweet(infos)
    update = updateProfilePicture(infos[3])
    return bool(publish and update and infos)

# https://github.com/Timoleroux/Weather-Bot#mainpymakeSchedulesValid
def makeSchedulesValid(schedules):
    """Make a schedule list in the right format to be readable by the autoRun function.

    Args:
        schedules (list): list of schedules

    Returns:
        list: list of formated schedules
    """
    valid_schedules = []
    schedules = [x for x in schedules if x != '']
    for schedule_ in schedules:

        schedule = schedule_.replace(' ', '')
        if 2 <= len(schedule) <= 5:
            schedule = re.split('[hH:]', schedule)

            if len(schedule) == 2:
                sch_hour = schedule[0]
                sch_min = schedule[1]

                if (sch_hour + sch_min).isdigit() and 0 <= int(sch_hour) < 24 and 0 <= int(sch_hour) < 60:
                    valid_schedule = '{0}h{1}'.format(schedule[0].rjust(2, '0'), schedule[1].zfill(2))
                    valid_schedules.append(valid_schedule)

    if len(schedules) != len(valid_schedules) != 0:
        logger.warning("Schedules have been removed because they are not valid.")

    return valid_schedules or False


def autoRun(city, schedules):
    """Publishes a Tweet based on information about a city and updates the profile picture only at certains times. 

    Args:
        city (str): name of a city
        schedules (list): list of schedules

    Returns:
        bool: False if an error occured, else run endlessly
    """

    valid_schedules = makeSchedulesValid(schedules)
    if valid_schedules:
        logger.info(f"Launch the automatic script for {city}. Schedules: {valid_schedules}")
    else:
        logger.error(f"No schedule is valid: {schedules}")
        return False


    while True:

        all_weather_infos = allWeatherInfos(city)

        if currentTime('%Hh%M') in valid_schedules and all_weather_infos != False:
            if not publishTweet(all_weather_infos):
                time.sleep(30)
                publishTweet(all_weather_infos)
            updateProfilePicture(all_weather_infos[3])

        time.sleep(60)

if __name__ == '__main__':
    manualRun(input('Pick a city'))
    # autoRun(input(input('Pick a city')), ['7h', '12h', '19h30'])