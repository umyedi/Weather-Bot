from ressources import AuthTweepy, AuthPyown, currentTime, CUR_DIR
import pyowm
import tweepy
import time
import logging
import sys
import re

# Configuration du format des messages de log
logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.FileHandler(filename='main.log', mode='a', encoding='UTF-8'),
                        logging.StreamHandler(sys.stdout),
                    ],
                    format='[%(asctime)s] %(levelname)s -> %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger()

# https://github.com/Timoleroux/Weather-Bot#mainpyallweatherinfos
def allWeatherInfos(city):
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
        logger.warning(f"La location pour '{city}' n'est pas valide ({e}).")
        return False
    except pyowm.commons.exceptions.APIRequestError as e:
        logger.warning(f"Veuillez entrez un nom de ville ({e}).")
        return False
    except pyowm.commons.exceptions.InvalidSSLCertificateError as e:
        logger.warning(f"Un programme externe bloque les connexions ({e}).")
        return False
    except pyowm.commons.exceptions.UnauthorizedError as e:
        logger.warning(f"Clé d'authentification Pyowm incorrect ({e}).")
        return False


# https://github.com/Timoleroux/Weather-Bot#mainpyupdateprofilpicture
def updateProfilPicture(weather):
    directory = CUR_DIR + '\\profil_pictures\\'

    if weather == 'ciel dégagé':
        AuthTweepy().update_profile_image(f'{directory}soleil.png')
    elif weather in ['couvert', 'peu nuageux', 'partiellement nuageux']:
        AuthTweepy().update_profile_image(f'{directory}couvert.png')
    elif weather == 'nuageux':
        AuthTweepy().update_profile_image(f'{directory}nuageux.png')
    elif weather == 'pluie modérée':
        AuthTweepy().update_profile_image(f'{directory}pluie.png')
    elif weather == 'légère pluie':
        AuthTweepy().update_profile_image(f'{directory}legere_pluie.png')
    elif weather in ['brume', 'brouillard']:
        AuthTweepy().update_profile_image(f'{directory}brume.png')
    elif weather == 'orageux':
        AuthTweepy().update_profile_image(f'{directory}orageux.png')
    else:
        print(logging.error(f"Aucune photo de profil correspond à '{weather}' pour le moment."))
        return False

    return True

# https://github.com/Timoleroux/Weather-Bot#mainpypublishtweet
def publishTweet(weather_infos):

    tweet = f"""
    Voici la météo pour {weather_infos[0]}, le {weather_infos[1]} à {weather_infos[2]}:
        ☀️ Temps : {weather_infos[3]}
        🌡️ Température moyenne : {weather_infos[4]}°C (ressenti {weather_infos[5]}°C)
        💨 Vitesse du vent : {weather_infos[6]} km/h"""

    try:
        AuthTweepy().update_status(tweet)
        logger.info("Tweet publié !")
        return tweet

    except tweepy.errors.Forbidden as e:
        logger.warning(f"Le Tweet que vous essayez de publier existe déjà ({e}).")
        return False

    except tweepy.errors.Unauthorized as e:
        logger.warning(f"Clés d'authentification Tweepy incorrects ({e}).")
        return False

# https://github.com/Timoleroux/Weather-Bot#mainpymanualrun
def manualRun(city):
    infos = allWeatherInfos(city)
    publish = publishTweet(infos)
    update = updateProfilPicture(infos[3])
    return bool(publish and update and infos)

# https://github.com/Timoleroux/Weather-Bot#mainpymakeSchedulesValid
def makeSchedulesValid(schedules):
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
        logger.warning("Des horaires ont été retirés car ils ne sont pas valides.")

    return valid_schedules or False


# https://github.com/Timoleroux/Weather-Bot#mainpyautorun
def autoRun(city, schedules):

    valid_schedules = makeSchedulesValid(schedules)
    if valid_schedules:
        logger.info(f"Lancement du script automatique pour {city}. Horaires : {valid_schedules}")
    else:
        logger.error(f"Aucun horaire n'est valide : {schedules}")
        return False


    while True:

        all_weather_infos = allWeatherInfos(city)

        if currentTime('%Hh%M') in valid_schedules and all_weather_infos != False:
            if not publishTweet(all_weather_infos):
                time.sleep(30)
                publishTweet(all_weather_infos)
            updateProfilPicture(all_weather_infos[3])

        time.sleep(60)

if __name__ == '__main__':
    manualRun(input('Entrez une ville'))
    # autoRun(input(input('Entrez une ville')), ['7h', '12h', '19h30'])
