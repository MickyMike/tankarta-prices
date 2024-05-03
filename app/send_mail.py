import logging
import smtplib
from email.mime.text import MIMEText

from config import GMAIL_USERNAME, GMAIL_PASSWORD

log = logging.getLogger(__name__)


def send_mail(recipients: list[str], subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["To"] = ", ".join(recipients)
    msg["From"] = f"{GMAIL_USERNAME}@gmail.com"

    log.info("Sending email to %s", recipients)

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    smtp_server.sendmail(msg["From"], recipients, msg.as_string())
    smtp_server.quit()
