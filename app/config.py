import os
from pathlib import Path


RECIPIENTS = ["mi.sta160@gmail.com"]
PRICES_FILE_PATH = Path("prices.txt")


# scraper section
TANKARTA_USERNAME = os.getenv("TANKARTA_USERNAME", "dummy_user")
TANKARTA_PASSWORD = os.getenv("TANKARTA_PASSWORD", "dummy_pass")

TANKARTA_LOGIN_PAGE = "https://business.tankarta.cz"

LOAD_TIMEOUT = 10  # s
LOAD_POLL_FREQUENCY = 1  # s


# mail section
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME", "dummy_user")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD", "dummy_password")
