from pyowm.utils.config import get_default_config
from pyowm import *
import tweepy
import os
from datetime import datetime

# Ressources
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

# https://github.com/Timoleroux/Weather-Bot#ressourcespycurrenttime
def currentTime(format):
   return datetime.now().strftime(format)

# Authentification for Tweepy
# https://github.com/Timoleroux/Weather-Bot#ressourcespyauthtweepy
def AuthTweepy():
   auth = tweepy.OAuth1UserHandler(
      "API Key", 
      "API Key Secret", 
      "Access Token", 
      "Access Token Secret"
   )
   return tweepy.API(auth)

# Authentification for Pyown
# https://github.com/Timoleroux/Weather-Bot#ressourcespyauthpyowm
def AuthPyown():
   config_dict = get_default_config()
   config_dict["language"] = "fr"
   return OWM("Token", config_dict)