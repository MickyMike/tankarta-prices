import logging
import time

from config import LOAD_TIMEOUT, LOAD_POLL_FREQUENCY, TANKARTA_USERNAME, TANKARTA_PASSWORD, TANKARTA_LOGIN_PAGE

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

log = logging.getLogger(__name__)


class NotLoaded(Exception):
    pass


def wait_for_load(driver: webdriver.Firefox, element: str, locator: str = By.ID) -> None:
    try:
        log.info("Waiting to load %s", element)
        element_present = ec.presence_of_element_located((locator, element))
        WebDriverWait(driver, timeout=LOAD_TIMEOUT, poll_frequency=LOAD_POLL_FREQUENCY).until(element_present)
    except TimeoutException:
        log.error("Finding element %s timeouted after %d seconds", element, LOAD_TIMEOUT)
        raise NotLoaded


def get_new_prices() -> str:
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    driver.get(TANKARTA_LOGIN_PAGE)

    try:
        wait_for_load(driver, "login")
    except NotLoaded:
        log.warning("Login page not loaded, retrying")
        driver.get(TANKARTA_LOGIN_PAGE)

    log.info("Filling in username")
    username_area = driver.find_element(By.ID, "login")
    username_area.send_keys(TANKARTA_USERNAME)

    log.info("Filling in password")
    password_area = driver.find_element(By.ID, "pwd")
    password_area.send_keys(TANKARTA_PASSWORD)

    log.info("Pressing submit button")
    login_button = driver.find_element(By.ID, "submit")
    ActionChains(driver).click(on_element=login_button).perform()

    try:
        wait_for_load(driver, element="//div[@data-widget='Price']", locator=By.XPATH)
    except NotLoaded:
        log.warning("Prices page not loaded, retrying to click the login button")
        login_button = driver.find_element(By.ID, "submit")
        ActionChains(driver).click(on_element=login_button).perform()
        wait_for_load(driver, element="//div[@data-widget='Price']", locator=By.XPATH)

    price_box = driver.find_element(By.XPATH, "//div[@data-widget='Price']")
    prices = price_box.text

    retry_counter = 1
    while not prices and retry_counter <= 10:
        log.info("Prices not loaded, retrying (%d/10)", retry_counter)
        time.sleep(1)
        price_box = driver.find_element(By.XPATH, "//div[@data-widget='Price']")
        prices = price_box.text
        retry_counter += 1

    driver.quit()

    return prices
