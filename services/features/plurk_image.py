import os
from dotenv import load_dotenv
from plurk_oauth import PlurkAPI
load_dotenv()

#Plurk Part
CONSUMER_KEY = os.getenv('plurk_App_key')
CONSUMER_SECRET = os.getenv('plurk_App_secret')
ACCESS_TOKEN = os.getenv('plurk_token')
ACCESS_TOKEN_SECRET = os.getenv('plurk_secret')

#Plurk API
plurk = PlurkAPI(CONSUMER_KEY, CONSUMER_SECRET)
plurk.authorize(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

