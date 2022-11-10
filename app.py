from ressources import AuthTweepy, AuthPyown, currentTime, CUR_DIR
import pyowm
import tweepy
from pyowm.owm import OWM
import time
import logging

# Configuration du format des messages de log
logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    encoding='utf-8',
                    filemode='a',
                    format='[%(asctime)s] %(levelname)s -> %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger()


# https://github.com/Timoleroux/Weather-Bot#apppyallweatherinfos
def allWeatherInfos(city):
    try:
        owm = AuthPyown()
        mgr = owm.weather_manager()

        location = mgr.weather_at_place(city)
        date = currentTime("%d/%m/%Y")
        time = currentTime("%Hh%M")
        weather = location.weather.detailed_status
        temp = location.weather.temperature('celsius')
        wind_speed = location.weather.wind().get('speed', 0)
        wind_speed = round(wind_speed*3.6, 2)
        return [city, date, time, weather, int(round(temp['temp'])), int(round(temp['feels_like'])), wind_speed]

    except pyowm.commons.exceptions.NotFoundError as e:
        logger.error(f"La location pour '{city}' n'est pas valide ({e}).")
        exit()
    except pyowm.commons.exceptions.InvalidSSLCertificateError as e:
        logger.error(f"Un programme externe bloque les connexions ({e}).")
        exit()
    except pyowm.commons.exceptions.UnauthorizedError as e:
        logger.error(f"Clé d'authentification Pyowm incorrect ({e}).")
        exit()


# https://github.com/Timoleroux/Weather-Bot#apppyupdateprofilpicture
def updateProfilPicture(weather):
    directory = CUR_DIR + '\\profil_pictures\\'

    if weather == 'ciel dégagé':
        AuthTweepy().update_profile_image(directory + 'ciel_degage.png')
    elif weather in ['couvert', 'peu nuageux', 'partiellement nuageux']:
        AuthTweepy().update_profile_image(directory + 'couvert.png')
    elif weather == 'nuageux':
        AuthTweepy().update_profile_image(directory + 'nuageux.png')
    elif weather == 'pluie modérée':
        AuthTweepy().update_profile_image(directory + 'pluie.png')
    elif weather == 'brume':
        AuthTweepy().update_profile_image(directory + 'brume.png')
    elif weather == 'orageux':
        AuthTweepy().update_profile_image(directory + 'orageux.png')
    else:
        print(logging.warn(f"Aucune photo de profile correspond à '{weather}' pour le moment."))
        return False

    return True

# https://github.com/Timoleroux/Weather-Bot#apppypublishtweet
def publishTweet(weather_infos):
    tweet = f"""
    Voici la météo pour {weather_infos[0]}, le {weather_infos[1]} à {weather_infos[2]}:
        ☀️ Temps : {weather_infos[3]}
        🌡️ Température moyenne : {weather_infos[4]}°C (ressenti {weather_infos[5]}°C)
        💨 Vitesse du vent : {weather_infos[6]} km/h"""

    try:
        AuthTweepy().update_status(tweet)
        return tweet
    except tweepy.errors.Forbidden as e:
        logger.error(f"Le Tweet que vous essayez de publier existe déjà ({e}).")
        exit()
    except tweepy.errors.Unauthorized as e:
        logger.error(f"Clés d'authentification Tweepy incorrects ({e}).")
        exit()

# https://github.com/Timoleroux/Weather-Bot#apppymanualrun
def manualRun():
    city = input("Entrez une ville : ")
    all_weather_infos = allWeatherInfos(city)

    logger.info("Tweet en cours de publication...")
    publishTweet(all_weather_infos)
    updateProfilPicture(all_weather_infos[3])
    logger.info("Tweet publié !")

    return True

# https://github.com/Timoleroux/Weather-Bot#apppyautorun
def autoRun(schedules):
    city = input("Entrez une ville : ")
    logging.info(f"Lancement du script automatique pour {city}. Horaires : {schedules}")

    while True:

        all_weather_infos = allWeatherInfos(city)

        if currentTime('%Hh%M') in schedules:

            logging.info(f"Tweet en cours de publication...")

            publishTweet(all_weather_infos)
            updateProfilPicture(all_weather_infos[3])

            logging.info(f"Tweet publié !")

        time.sleep(60)

autoRun(['21h20', '21h25', '21h30'])