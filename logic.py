from aiogram.types import InputFile

from db import Database
from datetime import datetime


async def mailing(bot):
    db = Database()
    await db.async_init()
    users = await db.get_all_users()
    product_infos = await db.get_only_new_products()
    if product_infos is not None:
        for chat_id in users:
            try:
                await bot.send_message(chat_id=chat_id, text="📨 Рассылка")
            except:
                print("blocked")
        for product_info in product_infos.values():
            message = ''
            if product_info['closedate'] == product_info['opendate']:
                message += "💰 Кэшбек дня\n"
            
            link_to_product = f"https://www.tinkoff.ru/bonuses/?offerId={product_info['id']}&from=004&parentCategory=004"
            if product_info['adverttexthtml'] != '':
                message += f"[{product_info['adverttexthtml']}]({link_to_product})\n"
            else:
                message += f"[{product_info['merchantname']}]({link_to_product})\n"

            message += f"Размер кэшбека: {product_info['cashbackpercent']}%\n"
            
            closedate_str = product_info['closedate']
            closedate_datetime = datetime.fromisoformat(closedate_str)
            formatted_date = closedate_datetime.strftime('%d.%m.%Y')
            message += f"Действует до {formatted_date}"
            image_path = f"src/{product_info['id']}.jpg"


            for chat_id in users:
                try:
                    with open(image_path, 'rb') as photo:
                        await bot.send_photo(chat_id=chat_id, photo=InputFile(photo), caption=message, parse_mode='Markdown')
                except:
                    print("user blocked bot")