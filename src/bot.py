import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, URLInputFile, CallbackQuery, Message

from utils import make_markup, send_notifications
from users import workers, run_users_clients

from config import *

from aiogram import Bot, Dispatcher, F

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML.value))

dp = Dispatcher()




async def on_startup():
    for worker in workers.values():
        user_is_working_msg = '<b>Вы не работаете❌</b>' if not worker.working else '<b>Вы работаете✅</b>'
        menu_msg = await bot.send_photo(worker.user_chat_id,
                             photo=URLInputFile(
                                 url='https://i.pinimg.com/550x/8e/67/24/8e672428f6fc29cc1bdfd6f9e45d30d4.jpg'),
                             caption=f'<b>🛠️ Настройки бота</b>\n<i>Выберите одно из действий ниже, чтобы настроить бота под свои нужды.</i>\n{user_is_working_msg}',
                             reply_markup=make_markup(working=worker.working))
        worker.menu_msg = menu_msg.message_id


async def on_shutdown():
    for worker in workers.values():
        await bot.delete_message(chat_id=worker.user_chat_id, message_id=worker.menu_msg)

@dp.message(CommandStart())
async def start(message: Message):
    worker = workers[message.from_user.id]
    user_is_working_msg = '<b>Вы не работаете❌</b>' if not worker.working else '<b>Вы работаете✅</b>'
    menu_msg = await bot.send_photo(worker.user_chat_id,
                                    photo=URLInputFile(
                                        url='https://i.pinimg.com/550x/8e/67/24/8e672428f6fc29cc1bdfd6f9e45d30d4.jpg'),
                                    caption=f'<b>🛠️ Настройки бота</b>\n<i>Выберите одно из действий ниже, чтобы настроить бота под свои нужды.</i>\n{user_is_working_msg}',
                                    reply_markup=make_markup(working=worker.working))
    worker.menu_msg = menu_msg.message_id
    await message.delete()


@dp.callback_query(F.data == 'stop')
async def stop_working(callback: CallbackQuery):
    worker = workers.get(callback.from_user.id)
    worker.working = False
    await callback.message.edit_caption(caption='<b>🛠️ Настройки бота</b>\n<i>Выберите одно из действий ниже, чтобы настроить бота под свои нужды.</i>\n<b>Вы не работаете❌</b>',
                                        reply_markup=make_markup(working=worker.working))


@dp.callback_query(F.data == 'start')
async def start_working(callback: CallbackQuery):
    worker = workers.get(callback.from_user.id)
    worker.working = True
    await callback.message.edit_caption(caption='<b>🛠️ Настройки бота</b>\n<i>Выберите одно из действий ниже, чтобы настроить бота под свои нужды.</i>\n<b>Вы работаете✅</b>',
                                             reply_markup=make_markup(working=worker.working))


@dp.callback_query(F.data == 'stop_notification')
async def stop_notification(callback: CallbackQuery):
    worker = workers.get(callback.from_user.id)
    worker.sender = False
    await callback.answer('❗️❗️Уведомления остановлены❗️❗️')


async def run_bot_client():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    asyncio.create_task(run_users_clients())
    for worker in workers.values():
        asyncio.create_task(send_notifications(bot=bot, worker=worker))
    await dp.start_polling(bot)

