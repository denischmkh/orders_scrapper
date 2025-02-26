import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
API_TOKEN = os.getenv('API_TOKEN')
USER_CHAT_ID = int(os.getenv('USER_CHAT_ID'))
TARGET_CHAT_ID = int(os.getenv('TARGET_CHAT_ID'))
MAIN_2FA = os.getenv('MAIN_2FA')

API_ID_2 = int(os.getenv('API_ID_2'))
API_HASH_2 = os.getenv('API_HASH_2')
PHONE_NUMBER_2 = os.getenv('PHONE_NUMBER_2')
PARTNER_2FA = os.getenv('PARTNER_2FA')
