from send_mail import send_mail
from scraper import get_prices

prices = get_prices()

send_mail(
    recipients=["mi.sta160@gmail.com"],
    subject="Pozor pozor, vyhlašuji nové ceny!",
    body=prices
)