import asyncio
from aiogram import types
from datetime import datetime

from db import Database


db = Database()
asyncio.get_event_loop().run_until_complete(db.async_init())


async def create_main_menu(chat_id):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_products = types.KeyboardButton("💵 Товары с кэшбеком")
    if await db.check_mailing_status(chat_id):
        btn_mailing = types.KeyboardButton("❌ Выключить рассылку")
    else:
        btn_mailing = types.KeyboardButton("✅ Включить рассылку")

    menu.add(btn_products, btn_mailing)
    return menu


async def create_mailing_markup():
    menu = types.InlineKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.InlineKeyboardButton("✅ Да", callback_data='yes')
    btn_no = types.InlineKeyboardButton("❌ Нет", callback_data='no')

    menu.add(btn_yes, btn_no)
    return menu


async def create_products_menu():
    products = await db.take_names_and_precents()

    inline_keyboard = types.InlineKeyboardMarkup()
    for product in products:
        date = product['closedate']
        date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M%z")
        formatted_date = date_object.strftime("%d.%m")
        button = types.InlineKeyboardButton(text=f"{product['merchantname']} - {product['cashbackpercent']}% до {formatted_date}", callback_data=str(product['id']))
        inline_keyboard.add(button)

    return inline_keyboard

