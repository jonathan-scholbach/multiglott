import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import config


def send_mail(
    sender_email: str, receiver_email: str, subject: str, html_body: str
):
    message = MIMEMultipart("html")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(html_body, "html"))

    port = 465
    password = config["SMTP_PASSWORD"]

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("test.jargon.app@gmail.com", password)
        server.sendmail(sender_email, receiver_email, message.as_string())
