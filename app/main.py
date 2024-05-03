import logging

from config import RECIPIENTS, PRICES_FILE_PATH
from send_mail import send_mail
from scraper import get_new_prices

log = logging.getLogger("main")
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


def get_old_prices() -> str:
    if PRICES_FILE_PATH.is_file():
        with open(PRICES_FILE_PATH, "r") as f:
            return f.read()
    else:
        return ""


def main() -> None:
    new_prices = get_new_prices()
    old_prices = get_old_prices()

    if not new_prices:
        log.warning("New prices were not obtained correctly")
        return

    if new_prices == old_prices:
        log.info("Prices are the same, no email will be sent")
        return

    with open(PRICES_FILE_PATH, "w") as f:
        f.write(new_prices)

    send_mail(
        recipients=RECIPIENTS,
        subject="Pozor pozor, vyhlašuji nové ceny!",
        body=new_prices
    )


if __name__ == '__main__':
    main()
