from pyowm import *
from pyowm.utils.config import get_default_config
import tweepy
import os
import random

# Ressources
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

# Authentification for Tweepy
def AuthTweepy():
   auth = tweepy.OAuth1UserHandler(
      "JsbBxBZAnxK9tPq7j7QoaJjPc", 
      "5McyvbrEa7XTVoxQ9mo77puIJaWmUN5aZqIpzreREBCjMMUBsw", 
      "1375740084117471236-beGVb4GL8B33S2NXj1omDeiPiw3VoJ", 
      "920exybamffJqxbFNPCGWazB7qbuaTAAoD4xvFUrVJJgL"
   )
   return tweepy.API(auth)

# Authentification for Pyown
def AuthPyown():
   config_dict = get_default_config()
   config_dict['language'] = 'fr'
   return OWM('ca34703d746615ba513984e5155d27a7', config_dict)