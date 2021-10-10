import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Sender:
    def __init__(self, to_email, message):
        self.to_email = to_email
        self.message = message

    def send_message(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--from_email", required=True, type=str)
        parser.add_argument("--password", required=True, type=str)
        args = parser.parse_args()

        msg = MIMEMultipart()
        to_email = self.to_email
        message = self.message

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(args.from_email, args.password)
        server.sendmail(args.from_email, to_email, msg.as_string())
        server.quit()
