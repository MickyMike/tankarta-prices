import os
import smtplib
from email.mime.text import MIMEText

GMAIL_USERNAME = os.getenv("GMAIL_USERNAME", "dummy_user")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD", "dummy_password")


def send_mail(recipients: list[str], subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["To"] = ", ".join(recipients)
    msg["From"] = f"{GMAIL_USERNAME}@gmail.com"

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    smtp_server.sendmail(msg["From"], recipients, msg.as_string())
    smtp_server.quit()
