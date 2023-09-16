from pyowm.utils.config import get_default_config
from pyowm import *
import os, datetime
import tweepy

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

def currentTime(format):
   return datetime.datetime.now().strftime(format)

# Authentification for Tweepy
def AuthTweepy():
   auth = tweepy.OAuth1UserHandler(
      "API_Key", 
      "API_Key_Secret", 
      "Access_Token", 
      "Access_Token_Secret"
   )
   return tweepy.API(auth)

# Authentification for Pyown
def AuthPyown():
   config_dict = get_default_config()
   config_dict["language"] = "fr"
   return OWM("Token", config_dict)