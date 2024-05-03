import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

USERNAME = os.getenv("TANKARTA_USERNAME", "dummy_user")
PASSWORD = os.getenv("TANKARTA_PASSWORD", "dummy_pass")


def get_prices() -> str:
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    driver.get("https://business.tankarta.cz")

    time.sleep(2)

    # fill in username
    username_area = driver.find_element(By.ID, "login")
    username_area.send_keys(USERNAME)

    # fill in password
    password_area = driver.find_element(By.ID, "pwd")
    password_area.send_keys(PASSWORD)

    # press login
    action = ActionChains(driver)
    login_button = driver.find_element(By.ID, "submit")
    action.click(on_element=login_button)
    action.perform()

    time.sleep(2)

    price_box = driver.find_element(By.XPATH, "//div[@data-widget='Price']")

    prices = price_box.text
    driver.quit()

    return prices
