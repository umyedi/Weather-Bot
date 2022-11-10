from ressources import AuthTweepy, AuthPyown, currentTime, CUR_DIR
from pyowm import *
import time

# https://github.com/Timoleroux/Weather-Bot#apppyallweatherinfos
def allWeatherInfos(city):
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

# https://github.com/Timoleroux/Weather-Bot#apppyupdateprofilpicture
def updateProfilPicture(weather):
    directory = CUR_DIR + '\\profil_pictures\\'

    match weather:
        case 'ciel dégagé':
            AuthTweepy().update_profile_image(directory + 'ciel_degage.png')
        case 'couvert':
            AuthTweepy().update_profile_image(directory + 'couvert.png')
        case 'peu nuageux':
            AuthTweepy().update_profile_image(directory + 'couvert.png')
        case 'partiellement nuageux':
            AuthTweepy().update_profile_image(directory + 'couvert.png')
        case 'nuageux':
            AuthTweepy().update_profile_image(directory + 'nuageux.png')
        case 'pluie modérée':
            AuthTweepy().update_profile_image(directory + 'pluie.png')
        case 'brume':
            AuthTweepy().update_profile_image(directory + 'brume.png')
        case 'orageux':
            AuthTweepy().update_profile_image(directory + 'orageux.png')
        case _:
            print(writeInLog(f"[{currentTime('%d/%m/%Y %H:%M:%S')}] Aucune photo de profile correspond à '{weather}' pour le moment."))
            return False
    return True

# https://github.com/Timoleroux/Weather-Bot#apppypublishtweet
def publishTweet(weather_infos):
    tweet = f"""
    Voici la météo pour {weather_infos[0]}, le {weather_infos[1]} à {weather_infos[2]}:
        ☀️ Temps : {weather_infos[3]}
        🌡️ Température moyenne : {weather_infos[4]}°C (ressenti {weather_infos[5]}°C)
        💨 Vitesse du vent : {weather_infos[6]} km/h"""

    AuthTweepy().update_status(tweet)
    return tweet

# https://github.com/Timoleroux/Weather-Bot#apppywriteinlog
def writeInLog(content):

    file_path = CUR_DIR + "\\LOG.txt"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + content)
    return content

# https://github.com/Timoleroux/Weather-Bot#apppymanualrun
def manualRun():
    city = input("Entrez une ville : ")
    all_weather_infos = allWeatherInfos(city)

    print(writeInLog(f"[{currentTime('%d/%m/%Y %H:%M:%S')}] Tweet en cours de publication..."))
    publishTweet(all_weather_infos)
    updateProfilPicture(all_weather_infos[3])
    print(writeInLog(f"[{currentTime('%d/%m/%Y %H:%M:%S')}] Tweet publié !"))
    return True

# https://github.com/Timoleroux/Weather-Bot#apppyautorun
def autoRun(schedules):

    city = input("Entrez une ville : ")
    print(writeInLog(f"[{currentTime('%d/%m/%Y %H:%M:%S')}] Lancement du script automatique pour {city}. Horaires : {schedules}"))

    while True:

        all_weather_infos = allWeatherInfos(city)

        if currentTime('%Hh%M') in schedules:

            print(writeInLog(f"[{currentTime('%d/%m/%Y %H:%M:%S')}] Tweet en cours de publication..."))

            publishTweet(all_weather_infos)
            updateProfilPicture(all_weather_infos[3])

            print(writeInLog(f"[{currentTime('%d/%m/%Y %H:%M:%S')}] Tweet publié !"))

        time.sleep(60)
