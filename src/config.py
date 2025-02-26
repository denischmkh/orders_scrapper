import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
API_TOKEN = os.getenv('API_TOKEN')
USER_CHAT_ID = int(os.getenv('USER_CHAT_ID'))
TARGET_CHAT_ID = int(os.getenv('TARGET_CHAT_ID'))