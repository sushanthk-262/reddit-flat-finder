import logging
import smtplib
from email.message import EmailMessage
import os

def send_mail(file_path):

    sender = os.environ["MAIL_SENDER"]
    password = os.environ["MAIL_PASSWORD"]
    receiver = os.environ["MAIL_RECEIVER"]

    msg = EmailMessage()
    msg["Subject"] = "Reddit Flat Finder Results"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content("Attached are latest filtered flat listings.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="csv",
            filename="matches.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    logging.info("Email sent")
