import requests
import json

from session_id_parser import extract_value_from_json_file


async def get_json(bot):
    url = "https://ms-gateway.tinkoff.ru/loyalty_api/api/internetBank/clientOffers"
    sessionid = extract_value_from_json_file()

    params = {
        'wuid': 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX',
        'appName': 'bonuses',
        'appVersion': '1.146.0',
        'sessionid': f'{sessionid}',
        'origin': 'web,ib5,platform'
    }

    headers = {
        'User-Agent': 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX',
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
        with open('response.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=4)
    else:
        print('Error: %s' % response.status_code)
