import json
import requests
from bs4 import BeautifulSoup
import os
import asyncio

from db import Database
from clear_src_folder import clear_src_folder

db = Database()
asyncio.get_event_loop().run_until_complete(db.async_init())

async def get_new_products(bot):
    if not os.path.exists('src'):
        os.makedirs('src')

    with open('response.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    result_dict = {}
    await clear_src_folder()

    if 'payload' in data and isinstance(data['payload'], list):
        payload_data = data['payload']

        for item in payload_data:
            if 'merchant' in item and 'merchantCategories' in item['merchant']:
                merchant = item['merchant']
                merchant_categories = merchant.get('merchantCategories', [])

                if any(category.get('category', {}).get('code') == '004' for category in merchant_categories):
                    advert_text = BeautifulSoup(item.get('advertTextHtml', ''), 'html.parser').get_text()

                    result_dict[item.get('id')] = {
                        'advertTextHtml': advert_text,
                        'merchantName': merchant.get('merchantName'),
                        'openDate': item.get('dates', {}).get('openDate'),
                        'closeDate': item.get('dates', {}).get('closeDate'),
                        'cashbackPercent': item.get('cashbackInfo', {}).get('cashbackPercent'),
                        'bigImage': item.get('image', {}).get('bigImage', '')
                    }

                    other_codes = set(category.get('category', {}).get('code') for category in merchant_categories)
                    if 'Cashback-day' in other_codes or 'new' in other_codes:
                        result_dict[item.get('id')]['otherCodes'] = other_codes

                    image_url = result_dict[item.get('id')]['bigImage']
                    if image_url:
                        response = requests.get(image_url)
                        image_filename = os.path.join('src', f"{item.get('id')}.jpg")
                        with open(image_filename, 'wb') as image_file:
                            image_file.write(response.content)

    await db.add_products(result_dict)
