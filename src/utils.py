import asyncio
import datetime

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from users import Worker


def make_markup(working: bool):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Работаю ✅', callback_data='stop') if working else InlineKeyboardButton(
                text='Не работаю ❌', callback_data='start')],
            [InlineKeyboardButton(text='Остановить уведомления 📲❌', callback_data='stop_notification')]
        ]
    )
    return markup


async def delete_notification_later(chat_id, message_id: int, bot: Bot) -> None:
    await asyncio.sleep(15)
    await bot.delete_message(chat_id, message_id=message_id)


async def send_notifications(bot: Bot, worker: Worker):
    now_time = datetime.datetime.now()
    while True:
        if worker.sender:
            msg = await bot.send_message(chat_id=worker.user_chat_id,
                                         text=f'🕒 <b>Новый заказ!\n\n📅Время: {now_time.hour}:{now_time.minute}:{now_time.second}</b>')
            asyncio.create_task(
                delete_notification_later(chat_id=worker.user_chat_id, message_id=msg.message_id, bot=bot))
            await asyncio.sleep(5)
        else:
            now_time = datetime.datetime.now()
            await asyncio.sleep(1)
