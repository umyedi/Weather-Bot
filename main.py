from utils import AuthPyown, tweepy_client, CUR_DIR
import pyowm
import tweepy
import logging
import time
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(
            filename=f"{CUR_DIR}\\data\\main.log", mode="a", encoding="UTF-8"
        ),
        logging.StreamHandler(sys.stdout),
    ],
    format="[%(asctime)s] %(levelname)s -> %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger()


class Tweet:
    directory = CUR_DIR + "\\profile_pictures\\"

    def __init__(self, city):
        """Initialize Tweet instance with given city.

        Args:
            city (str): City name
        """
        self.city = city.title()
        self.schedules = []
        (
            self.date,
            self.hour,
            self.weather,
            self.temp,
            self.feels_like,
            self.wind_speed,
            self.tweet,
        ) = [None] * 7
        self.updateWeatherStats()

    def __repr__(self):
        return (
            f"Tweet(city='{self.city}', schedules='{self.schedules}', date='{self.date}', hour='{self.hour}', weather='{self.weather}', "
            f"temp={self.temp}, feels_like={self.feels_like}, wind_speed={self.wind_speed}, tweet={repr(self.tweet)})"
        )

    def updateWeatherStats(self) -> bool:
        """Fetch latest weather data from PyOWM.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return self.weatherStats()
        except pyowm.commons.exceptions.NotFoundError as e:
            logger.warning(f"The location for '{self.city}' isn't valid ({e}).")
        except pyowm.commons.exceptions.APIRequestError as e:
            logger.warning(f"Please enter a city name ({e}).")
        except pyowm.commons.exceptions.InvalidSSLCertificateError as e:
            logger.warning(f"An external program blocks the connections ({e}).")
        except pyowm.commons.exceptions.UnauthorizedError as e:
            logger.warning(f"Incorrect Pyowm authentication key ({e}).")
        return False

    def weatherStats(self) -> bool:
        """Helper to actually fetch weather data from PyOWM.

        Returns:
            bool: True if successful, False otherwise
        """
        owm = AuthPyown()
        mgr = owm.weather_manager()

        location = mgr.weather_at_place(self.city)
        self.date = datetime.now().strftime("%d/%m/%Y")
        self.hour = datetime.now().strftime("%Hh%M")
        self.weather = location.weather.detailed_status
        temperature = location.weather.temperature("celsius")
        self.temp = int(round(temperature["temp"]))
        self.feels_like = int(round(temperature["feels_like"]))
        wind_speed = location.weather.wind().get("speed", 0)
        self.wind_speed = round(wind_speed * 3.6, 2)  # Converted in km/h
        return True

    def updateProfilePicture(self) -> bool:
        """Update Twitter profile picture based on weather.
        Since there's no way to change profile picture on Twitter API v2, this function is useless.

        Returns:
            bool: True if successful, False otherwise
        """
        switch = {
            "brouillard": f"{self.directory}mist.png",
            "brume": f"{self.directory}mist.png",
            "ciel dégagé": f"{self.directory}sunny.png",
            "couvert": f"{self.directory}overcast.png",
            "légère pluie": f"{self.directory}slightly_rainy.png",
            "légères chutes de neige": f"{self.directory}snowy.png",
            "nuageux": f"{self.directory}cloudy.png",
            "orageux": f"{self.directory}stormy.png",
            "partiellement nuageux": f"{self.directory}overcast.png",
            "peu nuageux": f"{self.directory}overcast.png",
            "pluie modérée": f"{self.directory}rainy.png",
        }

        image_path = switch.get(self.weather)
        if image_path is not None:
            # Supposed to update profile picture
            return True
        else:
            logger.error(f"No profile pictures match '{self.weather}' for now.")
            return False

    def publishTweet(self) -> bool:
        """Publish tweet with latest weather data.

        Returns:
            bool: True if successful, False otherwise
        """
        self.tweet = (
            f"Voici la météo pour {self.city}, le {self.date} à {self.hour} :\n\t"
            f"☀️ Temps : {self.weather}\n\t"
            f"🌡️ Température : {self.temp}°C (ressenti {self.feels_like}°C)\n\t"
            f"💨 Vitesse du vent : {self.wind_speed} km/h"
        )

        try:
            tweepy_client.create_tweet(text=self.tweet)
            logger.info("Tweet published !")
            return True
        except tweepy.errors.Forbidden as e:
            logger.warning(f"The Tweet you are trying to post already exists ({e}).")
        except tweepy.errors.Unauthorized as e:
            logger.warning(f"Incorrect Tweepy authentication keys ({e}).")
        return False

    def addSchedules(self, schedules):
        """Add formatted schedules to tweet at.

        Args:
            schedules (List[str]): List of schedules in HH:MM format
        """
        schedules = [i for i in schedules if i != ""]

        for schedule in schedules:
            h = int(schedule[:2])
            m = int(schedule[3:])
            if (0 < h < 24) and (0 < m < 60) and schedule[2] == ":":
                self.schedules.append(schedule)

        if len(self.schedules) < len(schedules):
            logger.warning(
                "Some schedules have been removed because they are not valid."
            )


class AutoTweet(Tweet):
    def __init__(self, city, schedules):
        super().__init__(city)
        super().addSchedules(schedules)

    def autoRun(self):
        """Automatically run update of the weather and tweet on schedule."""
        if not self.schedules:
            logger.error(f"No schedule is valid: {self.schedules}")
            return False

        logger.info(
            f"Launch the automatic script for {self.city}. Schedules: {self.schedules}"
        )

        while True:
            if datetime.now().strftime("%H:%M") in self.schedules:
                self.updateWeatherStats()
                self.publishTweet()
                self.updateProfilePicture()
            time.sleep(60)


if __name__ == "__main__":
    AutoTweet("paris", ["14:43"]).autoRun()
