from ressources import AuthTweepy, AuthPyown, CUR_DIR
from pyowm import *
from datetime import datetime
import time

def allWeatherInfos(city):
    owm = AuthPyown()
    mgr = owm.weather_manager()
    location = mgr.weather_at_place(city)

    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%Hh%M")
    weather = location.weather.detailed_status
    temp = location.weather.temperature('celsius')
    wind_speed = location.weather.wind().get('speed', 0)
    wind_speed = round(wind_speed*3.6, 2)
    return [city, date, time, weather, int(round(temp['temp'])), int(round(temp['feels_like'])), wind_speed]

def updateProfilPicture(weather):
    directory = CUR_DIR + '\\profil_pictures\\'

    match weather:
        case 'ciel dégagé':
            AuthTweepy().update_profile_image(directory + 'ciel_degage.png')
        case 'couvert':
            AuthTweepy().update_profile_image(directory + 'couvert.png')
        case 'nuageux':
            AuthTweepy().update_profile_image(directory + 'nuageux.png')
        case _:
            print(f"Aucune photo de profile correspond à {weather} pour le moment.")
            return False
    return True

def publishTweet(weather_infos):
    tweet = f"""
    Voici la météo pour {weather_infos[0]}, le {weather_infos[1]} à {weather_infos[2]}:
        ☀️ Temps : {weather_infos[3]}
        🌡️ Température moyenne : {weather_infos[4]}°C (ressenti {weather_infos[5]}°C)
        💨 Vitesse du vent : {weather_infos[6]} km/h"""

    AuthTweepy().update_status(tweet)
    return tweet

def manualRun():
    city = input("Entrez une ville : ")
    all_weather_infos = allWeatherInfos(city)
    publishTweet(all_weather_infos)
    updateProfilPicture(all_weather_infos[3])
    return True

def autoRun(schedules):

    city = input("Entrez une ville : ")

    while True:

        current_time = datetime.now().strftime("%Hh%M")
        all_weather_infos = allWeatherInfos(city)

        for i in schedules:

            if i == current_time:

                publishTweet(all_weather_infos)
                updateProfilPicture(all_weather_infos[3])

                print(f'Tweet publié le {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}')

        time.sleep(60)

autoRun(['09h00', '09h05', '09h10'])