import asyncio
import datetime
import logging
import os.path
import random
import sys

import pytz
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, BufferedInputFile, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telethon.errors import FloodError
from telethon import TelegramClient, events

from config import (API_TOKEN,
                    API_HASH,
                    TARGET_CHAT_ID,
                    API_ID,
                    PHONE_NUMBER,
                    ADMIN_CHAT_ID,
                    API_ID_2,
                    API_HASH_2,
                    PHONE_NUMBER_2,
                    MAIN_2FA,
                    PARTNER_2FA,
                    FIRST_PARTNER_NAME)

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML.value))

dp = Dispatcher()

client = TelegramClient('session_name', API_ID, API_HASH)

client2 = TelegramClient('session_name_2', API_ID_2, API_HASH_2)


sender = False

fishing_active = True

second_partner = True if API_ID_2 else None


menu_msg: types.Message | None = None


@client.on(events.NewMessage(chats=[TARGET_CHAT_ID, -1002351516242]))
async def handler(event):
    global fishing_active
    global sender
    if fishing_active:
        message = event.message
        # Проверка, если в тексте сообщения содержится "Нужны грузчики"
        if "нужны грузчики" in message.text.lower() and 'кто первый поставит “+“' in message.text.lower():
            # Отправляем ответ на сообщение
            await message.reply("+")
            sender = True
        elif "нужны грузчики" in message.text.lower() and 'напишите когда вы сможете быть на заказе' in message.text.lower():
            kyiv_tz = pytz.timezone('Europe/Kiev')
            time_now = datetime.datetime.now(kyiv_tz)
            time_in_20_minutes = time_now + datetime.timedelta(minutes=(20 + (10 - time_now.minute % 10)))
            time_str = time_in_20_minutes.strftime('%H:%M')
            await message.reply(f"{time_str}")
            sender = True
    else:
        return


@client2.on(events.NewMessage(chats=[TARGET_CHAT_ID, -1002351516242]))
async def handler2(event):
    global fishing_active
    global second_partner
    global sender
    if fishing_active and second_partner:
        await asyncio.sleep(1)
        message = event.message
        # Проверка, если в тексте сообщения содержится "Нужны грузчики"
        if "нужны грузчики" in message.text.lower() and 'кто первый поставит “+“' in message.text.lower():
            # Отправляем ответ на сообщение
            await message.reply("+")
            sender = True
        elif "нужны грузчики" in message.text.lower() and 'напишите когда вы сможете быть на заказе' in message.text.lower():
            kyiv_tz = pytz.timezone('Europe/Kiev')
            time_now = datetime.datetime.now(kyiv_tz)
            time_in_20_minutes = time_now + datetime.timedelta(minutes=(20 + (10 - time_now.minute % 10)))
            time_str = time_in_20_minutes.strftime('%H:%M')
            await message.reply(f"{time_str}")
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
    await callback.message.edit_reply_markup(reply_markup=make_markup())
    logging.info('Start fishing...')


@dp.callback_query(F.data == 'stop')
async def stop_fishing(callback: types.CallbackQuery):
    global fishing_active
    if not fishing_active:
        await callback.answer(text='Бот остановлен')
        return
    fishing_active = False  # Отключаем режим рыбалки
    await callback.message.edit_reply_markup(reply_markup=make_markup())
    logging.info('Fishing stopped...')


@dp.callback_query(F.data == 'with_partner')
async def remove_partner(callback: types.CallbackQuery):
    global second_partner
    if not second_partner:
        await callback.answer('❗️ Вы итак без партнера ❗️')
        return
    second_partner = False
    await callback.message.edit_reply_markup(reply_markup=make_markup())


@dp.callback_query(F.data == 'without_partner')
async def remove_partner(callback: types.CallbackQuery):
    global second_partner
    if second_partner:
        await callback.answer('❗️ Вы итак с партнером ❗️')
        return
    second_partner = True
    await callback.message.edit_reply_markup(reply_markup=make_markup())


@dp.callback_query(F.data == 'with_second_partner')
async def remove_partner(callback: types.CallbackQuery):
    global third_partner
    if not third_partner:
        await callback.answer('❗️ Вы итак без партнера ❗️')
        return
    third_partner = False
    await callback.message.edit_reply_markup(reply_markup=make_markup())


@dp.callback_query(F.data == 'without_second_partner')
async def remove_partner(callback: types.CallbackQuery):
    global third_partner
    if third_partner:
        await callback.answer('❗️ Вы итак с партнером ❗️')
        return
    third_partner = True
    await callback.message.edit_reply_markup(reply_markup=make_markup())


async def delete_notification_later(message_id: int) -> None:
    await asyncio.sleep(15)
    await bot.delete_message(ADMIN_CHAT_ID, message_id=message_id)


async def send_message():
    global sender
    now_time = datetime.datetime.now()
    while True:
        if sender:
            msg = await bot.send_message(chat_id=ADMIN_CHAT_ID,
                                         text=f'🕒 <b>Новый заказ!\n\n📅Время: {now_time.hour}:{now_time.minute}:{now_time.second}</b>')
            asyncio.create_task(delete_notification_later(msg.message_id))
            await asyncio.sleep(5)
        else:
            now_time = datetime.datetime.now()
            await asyncio.sleep(1)


def check_user_is_working(user_status) -> InlineKeyboardButton | None:
    match user_status:
        case True:
            return InlineKeyboardButton(text=f'{FIRST_PARTNER_NAME} ✅',callback_data='with_partner')
        case False:
            return InlineKeyboardButton(text=f'{FIRST_PARTNER_NAME} ◼️', callback_data='without_partner')
        case None:
            return None


def make_markup() -> InlineKeyboardMarkup:
    global fishing_active
    global second_partner
    if not fishing_active:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Включить ◼️', callback_data='start'),
                 InlineKeyboardButton(text='Выключить ❌', callback_data='stop')],
                [InlineKeyboardButton(text='Остановить уведомления 📲❌', callback_data='stop_notification')]
            ]
        )
        return markup
    else:
        partner_button = check_user_is_working(second_partner)
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Включить ✅', callback_data='start'),
                 InlineKeyboardButton(text='Выключить ◼️', callback_data='stop')],
                [partner_button if partner_button else InlineKeyboardButton(text='Не активен❌', callback_data='none')],
                [InlineKeyboardButton(text='Остановить уведомления 📲❌', callback_data='stop_notification')]
            ]
        )
        return markup



async def send_menu_to_user():
    global menu_msg
    msg = await bot.send_photo(ADMIN_CHAT_ID,
                               photo=URLInputFile(
                                   url='https://i.pinimg.com/550x/8e/67/24/8e672428f6fc29cc1bdfd6f9e45d30d4.jpg',
                                   filename='menu_image.png'),
                               caption='<b>🛠️ Настройки бота</b>\n<i>Выберите одно из действий ниже, чтобы настроить бота под свои нужды.</i>\n'
                                       '1.Кнопка "Выключить" представьте себе <b>❗️❗️❗️ВЫКЛЮЧАЕТ БОТА❗️❗️❗️</b>\n'
                                       '2.Кнопка "Остановить уведомления " Угадай ЧЕ? <b>❗️❗️❗️ВЫКЛЮЧАЕТ УВЕДОМЛЕНИЯ❗️❗️❗️</b>',
                               reply_markup=make_markup())
    menu_msg = msg

async def waiting_order():
    try:
        await client.start(PHONE_NUMBER, password=MAIN_2FA)
        await client2.start(PHONE_NUMBER_2, password=PARTNER_2FA)
    except (TypeError, ValueError):
        pass
    logging.info("Бот запущен и работает...")
    try:
        await asyncio.gather(
            client.run_until_disconnected(),
            client2.run_until_disconnected()
        )
    except ConnectionError:
        pass

async def on_shutdown():
    global menu_msg
    await bot.delete_message(ADMIN_CHAT_ID, message_id=menu_msg.message_id)


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
