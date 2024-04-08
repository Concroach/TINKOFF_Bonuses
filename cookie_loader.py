import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        return text, title

async def load_cookie(bot):
    cookies_file = "cookies.json"
    url = "https://www.tinkoff.ru/bonuses/004/"


    # Загрузка кук из файла
    try:
        with open(cookies_file, 'r') as f:
            cookies_list = json.load(f)
    except FileNotFoundError:
        cookies_list = []

    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}

    async with aiohttp.ClientSession(cookies=cookies_dict) as session:
        response_text, title = await fetch(session, url)

        if title:
            await bot.send_message(chat_id='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', text=f"{title} Заголовок")
        else:
            await bot.send_message(chat_id='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', text="ЗАГОЛОВОК СТРАНИЦЫ НЕ НАЙДЕН")

        new_cookies = session.cookie_jar.filter_cookies(url)

        new_cookies_list = [{'name': name, 'value': cookie.value} for name, cookie in new_cookies.items()]

    with open(cookies_file, 'w') as f:
        json.dump(new_cookies_list, f)
