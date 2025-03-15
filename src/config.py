import os

from dotenv import load_dotenv

load_dotenv()

API_1_ID = int(os.getenv('API_1_ID')) or None
API_1_HASH = os.getenv('API_1_HASH') or None
PHONE_1_NUMBER = os.getenv('PHONE_1_NUMBER') or None
USER_1_2FA = os.getenv('USER_1_2FA') or None
USER_1_CHAT_ID = os.getenv('USER_1_CHAT_ID') or None
USER_1_NAME = os.getenv('USER_1_NAME')


API_2_ID = int(os.getenv('API_2_ID')) or None
API_2_HASH = os.getenv('API_2_HASH') or None
PHONE_2_NUMBER = os.getenv('PHONE_2_NUMBER') or None
USER_2_2FA = os.getenv('USER_2_2FA') or None
USER_2_CHAT_ID = os.getenv('USER_2_CHAT_ID') or None
USER_2_NAME = os.getenv('USER_2_NAME')

BOT_TOKEN = os.getenv('BOT_TOKEN')

TARGET_CHAT_ID = int(os.getenv('TARGET_CHAT_ID'))