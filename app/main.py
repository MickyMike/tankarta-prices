import logging

from config import RECIPIENTS, PRICES_FILE_PATH
from send_mail import send_mail
from scraper import get_prices

log = logging.getLogger(__name__)


old_prices = ""
new_prices = get_prices()

if PRICES_FILE_PATH.is_file():
    with open(PRICES_FILE_PATH, "r") as f:
        old_prices = f.read()

if new_prices != old_prices:
    with open(PRICES_FILE_PATH, "w") as f:
        f.write(new_prices)

    send_mail(
        recipients=RECIPIENTS,
        subject="Pozor pozor, vyhlašuji nové ceny!",
        body=new_prices
    )
