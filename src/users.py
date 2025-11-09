import asyncio
import datetime

import pytz
from telethon import TelegramClient, events
from config import *


class Worker:
    def __init__(self, api_id, api_hash, phone_number, user_2fa, user_chat_id, user_name, working=False):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.user_2fa = user_2fa
        self.user_chat_id = int(user_chat_id)
        self.user_name = user_name
        self.working = working
        self.sender = False
        self.menu_msg = None
        self.client = TelegramClient(api_id=api_id,
                                     api_hash=api_hash,
                                     session=user_name)

    async def start(self):
        await self.client.start(phone=self.phone_number, password=self.user_2fa)
        self.client.add_event_handler(callback=self.handler,
                                      event=events.NewMessage(chats=[TARGET_CHAT_ID, -1002351516242]))
        await self.client.run_until_disconnected()

    async def handler(self, event):
        if self.user_chat_id != 680650067:
            await asyncio.sleep(1)
        if self.working:
            message = event.message
            if "нужны грузчики" in message.text.lower() and 'кто первый поставит “+“' in message.text.lower():
                await message.reply("+")
                self.sender = True
            elif "нужны грузчики" in message.text.lower() and 'напишите когда вы сможете быть на заказе' in message.text.lower():
                kyiv_tz = pytz.timezone('Europe/Kiev')
                time_now = datetime.datetime.now(kyiv_tz)
                time_in_20_minutes = time_now + datetime.timedelta(minutes=(30 + (10 - time_now.minute % 10)))
                time_str = time_in_20_minutes.strftime('%H:%M')
                await message.reply(f"{time_str}")
                self.sender = True


worker1 = Worker(api_id=API_1_ID,
               api_hash=API_1_HASH,
               phone_number=PHONE_1_NUMBER,
               user_2fa=USER_1_2FA,
               user_chat_id=USER_1_CHAT_ID,
               user_name=USER_1_NAME
               )

worker2 = Worker(api_id=API_2_ID,
               api_hash=API_2_HASH,
               phone_number=PHONE_2_NUMBER,
               user_2fa=USER_2_2FA,
               user_chat_id=USER_2_CHAT_ID,
               user_name=USER_2_NAME
               )

WORKERS_LIST = [worker1, worker2]


workers = {
    worker.user_chat_id: worker for worker in WORKERS_LIST
}


async def run_users_clients():
    tasks = [worker.start() for worker in workers.values()]
    await asyncio.gather(*tasks)


