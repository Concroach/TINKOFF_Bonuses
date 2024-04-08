import json

def extract_value_from_json_file():
    with open('cookies.json', 'r') as file:
        cookies = json.load(file)

    target_cookie_value = None
    for cookie in reversed(cookies):
        if "prod" in cookie.get("value", "") and "api" in cookie.get("value", ""):
            target_cookie_value = cookie["value"]
            break

    return target_cookie_value
