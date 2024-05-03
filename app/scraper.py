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


def wait_for_load(driver: webdriver.Firefox, element: str, locator: str = By.ID) -> None:
    try:
        log.info("Waiting to load %s", element)
        login_present = ec.presence_of_element_located((locator, element))
        WebDriverWait(driver, timeout=LOAD_TIMEOUT, poll_frequency=LOAD_POLL_FREQUENCY).until(login_present)
    except TimeoutException:
        log.exception("Finding element %s timeouted after %d seconds: ", element, LOAD_TIMEOUT)
        driver.quit()


def get_prices() -> str:
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    driver.get(TANKARTA_LOGIN_PAGE)

    wait_for_load(driver, "login")

    log.info("Filling in username")
    username_area = driver.find_element(By.ID, "login")
    username_area.send_keys(TANKARTA_USERNAME)

    log.info("Filling in password")
    password_area = driver.find_element(By.ID, "pwd")
    password_area.send_keys(TANKARTA_PASSWORD)

    log.info("Pressing submit button")
    action = ActionChains(driver)
    login_button = driver.find_element(By.ID, "submit")
    action.click(on_element=login_button)
    action.perform()

    time.sleep(0.2)  # give selenium time to click the button before waiting for price element
    wait_for_load(driver, element="//div[@data-widget='Price']", locator=By.XPATH)

    price_box = driver.find_element(By.XPATH, "//div[@data-widget='Price']")

    prices = price_box.text
    driver.quit()

    return prices
