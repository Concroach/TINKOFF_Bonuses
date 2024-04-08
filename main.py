import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram import executor
from aiogram.utils import executor
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import Database
from markup import *
from cookie_loader import load_cookie
from cookie_saver import save_cookie
from bonuses_json_parser import get_json
from info_json_parser import get_new_products
from logic import mailing

API_TOKEN = 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = Database()
asyncio.get_event_loop().run_until_complete(db.async_init())

all_ids_of_products = asyncio.get_event_loop().run_until_complete(db.take_all_ids()) 

sheduler_load_cookie = AsyncIOScheduler()
sheduler_get_new_products = AsyncIOScheduler()
sheduler_mailing = AsyncIOScheduler()
sheduler_products = AsyncIOScheduler()



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    username = f'@{message.chat.username}'
    if await db.user_exists(chat_id):
        markup = await create_main_menu(chat_id)
        await bot.send_message(chat_id=message.chat.id, text="С возвращением!", reply_markup=markup)
    else:
        markup = await create_mailing_markup()
        await bot.send_message(message.chat.id, text="Привет, ты хочешь получать рассылку о новых акциях и кэшбеке дня?", reply_markup=markup)
        await db.add_user(chat_id, username)
 

@dp.message_handler(lambda message: message.text == '💵 Товары с кэшбеком')
async def handle_cashback_button(message: types.Message):
    chat_id = message.chat.id
    markup = await create_products_menu()
    await bot.send_message(chat_id=chat_id, text=f"🤑 Товары с кэшбеком\nДля более подробной информации нажмите на интересующий товар", reply_markup=markup)


@dp.message_handler(lambda message: message.text == '❌ Выключить рассылку')
async def handle_cashback_button(message: types.Message):
    chat_id = message.chat.id
    await db.add_mailing_status(chat_id, False)
    markup = await create_main_menu(chat_id)
    await bot.send_message(chat_id, text="😿 Рассылка выключена", reply_markup=markup)


@dp.message_handler(lambda message: message.text == '✅ Включить рассылку')
async def handle_cashback_button(message: types.Message):
    chat_id = message.chat.id
    await db.add_mailing_status(chat_id, True)
    markup = await create_main_menu(chat_id)
    await bot.send_message(chat_id, text="😻 Рассылка включена", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in ["yes", "no"])
async def process_callback(call: types.CallbackQuery):
    cl = call.data
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    if cl == "yes":
        await db.add_mailing_status(chat_id, True)
    else:
        await db.add_mailing_status(chat_id, False)
    markup = await create_main_menu(chat_id)
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✔️ Выбор сохранен")
    await bot.send_message(chat_id=chat_id, text="🎉 Регистрация завершена\nКогда сэкономите миллион, не забудьте поделиться с автором бота!", reply_markup=markup)
    markup = await create_products_menu()
    await bot.send_message(chat_id=chat_id, text=f"🤑 Товары с кэшбеком\nДля более подробной информации нажмите на интересующий товар", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in all_ids_of_products)
async def process_callback(call: types.CallbackQuery):
    product_id = int(call.data)
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    product_info = await db.get_product_by_id(product_id)
    message = ''
    if product_info['closedate'] == product_info['opendate']:
        message += "💰 Кэшбек дня\n"
    
    link_to_product = f"https://www.tinkoff.ru/bonuses/?offerId={product_id}&from=004&parentCategory=004"
    if product_info['adverttexthtml'] != '':
        message += f"[{product_info['adverttexthtml']}]({link_to_product})\n"
    else:
        message += f"[{product_info['merchantname']}]({link_to_product})\n"

    message += f"Размер кэшбека: {product_info['cashpercent']}%\n"
    
    closedate_str = product_info['closedate']
    closedate_datetime = datetime.fromisoformat(closedate_str)
    formatted_date = closedate_datetime.strftime('%d.%m.%Y')
    message += f"Действует до {formatted_date}"
    image_path = f"src/{product_id}.jpg"

    with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id=chat_id, photo=InputFile(photo), caption=message, parse_mode='Markdown')
    markup = await create_products_menu()
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"🤑 Товары с кэшбеком \nДля более подробной информации нажмите на интересующий товар", reply_markup=markup)
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"🤑 Товары с кэшбеком\nДля более подробной информации нажмите на интересующий товар", reply_markup=markup)


@dp.message_handler(commands=['an'])
async def func_now_analytic(message):
    if message.chat.id == 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX':
        total_users = await db.count_users()
        await message.reply(f"Юзеров в бд: {total_users}")


@dp.callback_query_handler(lambda call: call.data.isdigit())
async def process_callback(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    markup = await create_products_menu()
    await bot.send_message(chat_id=chat_id, text=f"Данный товар уже не участвует в акции, вот актуальный список\n🤑 Товары с кэшбеком \nДля более подробной информации нажмите на интересующий товар", reply_markup=markup)


async def reload_products(bot):
    await get_json(bot)
    await get_new_products(bot)


async def products_sheduler(bot, hour, minute):
    print(1)
    sheduler_load_cookie.add_job(save_cookie, 'cron', hour=hour, minute=minute + 2, args=[bot])
    sheduler_load_cookie.add_job(load_cookie, 'cron', hour=hour, minute=minute + 6, args=[bot])
    sheduler_get_new_products.add_job(reload_products, 'cron', hour=hour, minute=minute + 9, args=[bot])

hour = 21
minute = 10
sheduler_products.add_job(products_sheduler, 'cron', hour=hour, minute=minute, args=[bot, hour, minute])
# sheduler_load_cookie.add_job(save_cookie, 'cron', hour=12, minute=0, args=[bot])
# sheduler_load_cookie.add_job(load_cookie, 'cron', hour=12, minute=5, args=[bot])
# sheduler_get_new_products.add_job(reload_products, 'cron', hour=12, minute=7, args=[bot])
sheduler_mailing.add_job(mailing, 'cron', hour=10, minute=30, args=[bot])

if __name__ == '__main__':
    sheduler_load_cookie.start()
    sheduler_get_new_products.start()
    sheduler_mailing.start()
    sheduler_products.start()
    executor.start_polling(dp, skip_updates=False)

# bonuses_par (session_par) -> info_json_par (clear_src)