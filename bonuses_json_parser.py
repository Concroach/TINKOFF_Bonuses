import requests
import json

from session_id_parser import extract_value_from_json_file


async def get_json(bot):
    print('start get_json')
    url = "https://ms-gateway.tinkoff.ru/loyalty_api/api/internetBank/clientOffers"
    sessionid = extract_value_from_json_file()
    params = {
        'wuid': 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX',
        'appName': 'bonuses',
        'appVersion': '1.146.0',
        'sessionid': f'{sessionid}',
        'origin': 'web,ib5,platform'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tinkoff.ru/',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.tinkoff.ru',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        # Сохранение ответа в файл
        with open('response.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=4)
        await bot.send_message(chat_id='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', text="Ответ успешно сохранен в файл 'response.json'")
    else:
        await bot.send_message(chat_id='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', text=f"Ошибка при выполнении запроса. Код статуса: {response.status_code}")

