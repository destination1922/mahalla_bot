import uvicorn
import requests
import threading
from config import *
from typing import List
from aiogram import types, Bot
from fastapi import FastAPI
from pydantic import BaseModel

bot = Bot(token=BOT_TOKEN)
app = FastAPI()


class User(BaseModel):
    phone: str
    text: str | None = None
    url: str | None = None


class Users(BaseModel):
    users: List[User]
    text: str | None
    url: str | None


@app.post('/send_notify')
async def bot_sender(data: Users):
    users = data.users
    text = data.text if data.text else "Message is empty"
    url = data.url
    if users:
        not_sent_users = ""
        for user in users:
            r_data = requests.get(f"{BASIC_API}get_user_id?phone={user.phone}")
            data = r_data.json()
            try: user_id = data['data']['telegram_id']
            except KeyError: user_id = None
            if user_id:
                r_lang = requests.get(f"{BASIC_API}lang_get?telegram_id={user_id}")
                lang_data = r_lang.json()
                lang = lang_data['data']
                if user.text and user.url:
                    i_text, i_url = user.text, user.url
                elif user.text or user.url:
                    i_text = user.text if user.text else text
                    i_url = user.url if user.url else url
                else: i_text, i_url = text, url
                if i_url:
                    btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text=VIEW_DOC[lang], url=i_url))
                    await bot.send_message(chat_id=user_id, text=i_text, reply_markup=btn)
                else:
                    await bot.send_message(chat_id=user_id, text=i_text)
            else:
                not_sent_users += f"{user.phone}, "
        if not_sent_users == "":
            return {"success": True}
        else:
            await bot.send_message(chat_id=1456374097, text=f"Unknown users: {not_sent_users}")
            return {"message": f"{not_sent_users} >> telefon raqam egalari bot dan foydalanmagan!"}
    else:
        return {"success": False, "message": "Users must not be empty"}


class MahallaWeb(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(MahallaWeb, self).__init__(*args, **kwargs)

    def run(self):
        uvicorn.run(
            'web:app',
            host='localhost',
            port=8000
        )