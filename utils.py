from pyowm.utils.config import get_default_config
from pyowm import OWM
import os
import tweepy

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

# Authentification for Tweepy
tweepy_client = tweepy.Client(
   bearer_token="bearer_token",
   consumer_key="consumer_key",
   consumer_secret="consumer_secret",
   access_token="access_token",
   access_token_secret="access_token_secret",
   wait_on_rate_limit=True,
)


# Authentification for Pyown
def AuthPyown():
   config_dict = get_default_config()
   config_dict["language"] = "fr"
   return OWM("api_token", config_dict)
