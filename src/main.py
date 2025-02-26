import asyncio
import datetime
import logging
import os.path
import random
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, BufferedInputFile, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telethon.errors import FloodError
from telethon import TelegramClient, events

from config import API_TOKEN, API_HASH, TARGET_CHAT_ID, API_ID, PHONE_NUMBER, USER_CHAT_ID, API_ID_2, API_HASH_2, PHONE_NUMBER_2, MAIN_2FA, PARTNER_2FA

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML.value))

dp = Dispatcher()

client = TelegramClient('session_name', API_ID, API_HASH)

client2 = TelegramClient('session_name_2', API_ID_2, API_HASH_2)

sender = False

fishing_active = True
with_partner_fishing = True

menu_msg: types.Message | None = None


@client.on(events.NewMessage(chats=[TARGET_CHAT_ID, -1002351516242]))
async def handler(event):
    global fishing_active
    if fishing_active:
        message = event.message
        # Проверка, если в тексте сообщения содержится "Нужны грузчики"
        if "Нужны грузчики" in message.text:
            # Отправляем ответ на сообщение
            await message.reply("+")
            global sender
            sender = True
    else:
        return


@client2.on(events.NewMessage(chats=[TARGET_CHAT_ID, -1002351516242]))
async def handler2(event):
    global fishing_active
    global with_partner_fishing
    if fishing_active and with_partner_fishing:
        await asyncio.sleep(1)
        message = event.message
        # Проверка, если в тексте сообщения содержится "Нужны грузчики"
        if "Нужны грузчики" in message.text:
            # Отправляем ответ на сообщение
            await message.reply("+")
            global sender
            sender = True
    else:
        return


@client.on(events.NewMessage(pattern=r"\.type ", from_users="me"))
async def type_message(event):
    orig_text = event.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "_"
    while tbp != orig_text:
        try:
            await event.edit(tbp + typing_symbol)
            await asyncio.sleep(0.1)
            if text[0] == ' ':
                await asyncio.sleep(1)
            tbp = tbp + text[0]
            text = text[1:]

            await event.edit(tbp)
            await asyncio.sleep(0.1)
        except FloodError as e:
            await asyncio.sleep(3)



async def waiting_order():
    await client.start(PHONE_NUMBER, password=MAIN_2FA)
    await client2.start(PHONE_NUMBER_2, password=PARTNER_2FA)
    logging.info("Бот запущен и работает...")
    await asyncio.gather(
        client.run_until_disconnected(),
        client2.run_until_disconnected()
    )


@dp.callback_query(F.data == 'stop_notification')
async def stop_sender(callback: types.CallbackQuery):
    global sender
    if not sender:
        await callback.answer(text='❗️ Уведомления уже отключены ❗️')
    sender = False  # Отключаем отправку сообщений
    await callback.answer(text='❌ Уведомления Отключены ❌')
    logging.info('Stopped notifications')


@dp.callback_query(F.data == 'start')
async def start_fishing(callback: types.CallbackQuery):
    global fishing_active
    if fishing_active:
        await callback.answer(text='Бот запущен')
        return
    fishing_active = True
    await callback.message.edit_reply_markup(reply_markup=make_startup_markup())
    logging.info('Start fishing...')


@dp.callback_query(F.data == 'stop')
async def stop_fishing(callback: types.CallbackQuery):
    global fishing_active
    if not fishing_active:
        await callback.answer(text='Бот остановлен')
        return
    fishing_active = False  # Отключаем режим рыбалки
    await callback.message.edit_reply_markup(reply_markup=make_stop_fishing_markup())
    logging.info('Fishing stopped...')

@dp.callback_query(F.data == 'with_partner')
async def remove_partner(callback: types.CallbackQuery):
    global with_partner_fishing
    if not with_partner_fishing:
        await callback.answer('❗️ Вы итак без партнера ❗️')
        return
    with_partner_fishing = False
    await callback.message.edit_reply_markup(reply_markup=make_without_partner_markup())

@dp.callback_query(F.data == 'without_partner')
async def remove_partner(callback: types.CallbackQuery):
    global with_partner_fishing
    if with_partner_fishing:
        await callback.answer('❗️ Вы итак с партнером ❗️')
        return
    with_partner_fishing = True
    await callback.message.edit_reply_markup(reply_markup=make_startup_markup())

async def delete_notification_later(message_id: int) -> None:
    await asyncio.sleep(15)
    await bot.delete_message(USER_CHAT_ID, message_id=message_id)


async def send_message():
    global sender
    now_time = datetime.datetime.now()
    while True:
        if sender:
            msg = await bot.send_message(chat_id=USER_CHAT_ID,
                                         text=f'🕒 <b>Новый заказ!\n\n📅Время: {now_time.hour}:{now_time.minute}:{now_time.second}</b>')
            asyncio.create_task(delete_notification_later(msg.message_id))
            await asyncio.sleep(5)
        else:
            now_time = datetime.datetime.now()
            await asyncio.sleep(1)


def make_startup_markup() -> InlineKeyboardMarkup:
    global with_partner_fishing
    partner_button = [InlineKeyboardButton(text='С Ильей 🐴 ✅', callback_data='with_partner')] if with_partner_fishing else [InlineKeyboardButton(text='Без Ильи 🐴 ❌', callback_data='without_partner')]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Включить ✅', callback_data='start'),
             InlineKeyboardButton(text='Выключить ◼️', callback_data='stop')],
            partner_button,
            [InlineKeyboardButton(text='Остановить уведомления 📲❌', callback_data='stop_notification')]
        ]
    )
    return markup

def make_without_partner_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Включить ✅', callback_data='start'),
             InlineKeyboardButton(text='Выключить ◼️', callback_data='stop')],
            [InlineKeyboardButton(text='Без Ильи 🐴 ❌', callback_data='without_partner')],
            [InlineKeyboardButton(text='Остановить уведомления 📲❌', callback_data='stop_notification')]
        ]
    )
    return markup

def make_stop_fishing_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Включить ◼️', callback_data='start'),
             InlineKeyboardButton(text='Выключить ❌', callback_data='stop')],
            [InlineKeyboardButton(text='Остановить уведомления 📲❌', callback_data='stop_notification')]
        ]
    )
    return markup


async def send_menu_to_user():
    global menu_msg
    msg = await bot.send_photo(USER_CHAT_ID,
                               photo=URLInputFile(url='https://i.pinimg.com/550x/8e/67/24/8e672428f6fc29cc1bdfd6f9e45d30d4.jpg',
                                                       filename='menu_image.png'),
                               caption='<b>🛠️ Настройки бота</b>\n<i>Выберите одно из действий ниже, чтобы настроить бота под свои нужды.</i>',
                               reply_markup=make_startup_markup())
    menu_msg = msg


async def on_shutdown():
    global menu_msg
    await bot.delete_message(USER_CHAT_ID, message_id=menu_msg.message_id)


async def on_startup():
    asyncio.create_task(send_menu_to_user())
    asyncio.create_task(waiting_order())
    asyncio.create_task(send_message())


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        logging.info('Stopping')
        sys.exit()
