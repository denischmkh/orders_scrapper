import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
API_TOKEN = os.getenv('API_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))
TARGET_CHAT_ID = int(os.getenv('TARGET_CHAT_ID'))
MAIN_2FA = os.getenv('MAIN_2FA')

API_ID_2 = int(os.getenv('API_ID_2') or 0) if os.getenv("API_ID_2") else None
API_HASH_2 = os.getenv('API_HASH_2') or None
PHONE_NUMBER_2 = os.getenv('PHONE_NUMBER_2') or None
PARTNER_2FA = os.getenv('PARTNER_2FA') or None
FIRST_PARTNER_NAME = os.getenv('FIRST_PARTNER_NAME') or None

