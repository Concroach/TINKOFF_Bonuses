from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

from mail import extract_code

async def save_cookie(bot):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.tinkoff.ru/bonuses/004/")
        time.sleep(5)

        phone_input = driver.find_element(By.NAME, "phone")
        phone_input.send_keys("'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'")

        time.sleep(3)

        code_input = driver.find_element(By.CSS_SELECTOR, 'button[automation-id="button-submit"]').click()
        time.sleep(47)
        sms = driver.find_element(By.CSS_SELECTOR, 'button[automation-id="resend-button"]').click()
        time.sleep(30)
        sms_code = await extract_code()
        time.sleep(20)

        button = driver.find_element(By.NAME, 'otp')
        button.send_keys(sms_code)
        time.sleep(5)

        # phone_input1 = driver.find_element(By.NAME, 'password')
        # phone_input1.send_keys("Merkoncel_")
        # code_input = driver.find_element(By.CSS_SELECTOR, 'button[automation-id="button-submit"]').click()

        time.sleep(3)
        phone_input1 = driver.find_element(By.ID, "pinCode0")
        phone_input1.send_keys("'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'")
        phone_input2 = driver.find_element(By.ID, "pinCode1")
        phone_input2.send_keys("'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'")
        phone_input3 = driver.find_element(By.ID, "pinCode2")
        phone_input3.send_keys("'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'")
        phone_input4 = driver.find_element(By.ID, "pinCode3")
        phone_input4.send_keys("'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'")
        button = driver.find_element(By.CSS_SELECTOR, 'button[automation-id="button-submit"]').click()
        time.sleep(7)

        # driver.refresh()
        cookies = driver.get_cookies()
    finally:
        html_code = driver.page_source

        with open("index.html", "w", encoding="utf-8") as file:
            file.write(html_code)
        driver.get_screenshot_as_file('file.png')

    with open("cookies.json", "w") as f:
        json.dump(cookies, f)
        await bot.send_message(chat_id='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', text=f"cookies.json DONE")

    driver.quit()
