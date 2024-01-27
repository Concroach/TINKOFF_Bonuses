import json
import asyncio
import httpx
from bs4 import BeautifulSoup

async def load_cookie(bot):
    async with httpx.AsyncClient() as client:
        with open("cookies.json", "r") as f:
            cookies_str = f.read()

        cookies = json.loads(cookies_str)

        response = await client.get("https://www.tinkoff.ru/bonuses/004/", cookies=cookies)
        await asyncio.sleep(5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.title

        if title_tag:
            print("Заголовок страницы после входа:", title_tag.string.strip())
        else:
            print("Заголовок страницы не найден")

        new_cookies = {cookie['name']: cookie['value'] for cookie in response.cookies}
        cookies.update(new_cookies)

        with open("cookies.json", "w") as f:
            json.dump(cookies, f)
