import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from .config_reader import config
from flask import current_app
import schedule
from threading import Thread
import time
import requests
from ..models.user import User
from app.__init__ import create_app
import json



logging.basicConfig(level=logging.INFO)

def create_bot(app):
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Hello!")

    def send_daily_messages():
        try:
            with app.app_context():
                from app.models.user import User
                users = User.query.filter(User.tgid.isnot(None)).all()

                for user in users:
                    try:
                        group_id = user.group
                        response = requests.get(f'http://localhost:5000/api/schedule/{group_id}')
                        if response.status_code == 200:
                            schedule_data = response.json()
                            formatted_json = json.dumps(schedule_data, indent=4, ensure_ascii=False)
                            message_text = f"Доброе утро! Вот ваше расписание на сегодня:\n{json.loads(formatted_json)}"
                        else:
                            message_text = "Доброе утро! Не удалось получить расписание."
                        
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(send_async_message(user.tgid, message_text))
                        loop.close()
                        
                    except Exception as e:
                        print(f"Ошибка отправки пользователю {user.tgid}: {e}")
        except Exception as e:
            print(f"Общая ошибка в send_daily_messages: {e}")

    async def send_async_message(chat_id, message):
        try:
            async with Bot(token=config.bot_token.get_secret_value()) as bot:
                await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {chat_id}: {e}")

    schedule.every().day.at("05:00").do(send_daily_messages)
    #schedule.every(1).minutes.do(send_daily_messages)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    async def main():
        await dp.start_polling(bot)

    if __name__ == "__main__":
        scheduler_thread = Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
    
        asyncio.run(main())