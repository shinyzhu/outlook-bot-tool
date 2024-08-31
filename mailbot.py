import os

from dotenv import load_dotenv

load_dotenv()

import logging

logging.basicConfig(level=logging.INFO)

from outlook_auth import auth_device_flow

import imaplib, smtplib, email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def decode_str(string):
    decoded, encoding = decode_header(string)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or "utf-8")
    return decoded


def fetch_emails():
    imap_server = os.getenv("OUTLOOK_IMAP_SERVER")
    imap_port = os.getenv("OUTLOOK_IMAP_PORT")
    user_email = os.getenv("OUTLOOK_USERNAME")

    access_token = auth_device_flow()

    imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap_conn.authenticate(
        "XOAUTH2", lambda x: f"user={user_email}\1auth=Bearer {access_token}\1\1"
    )
    imap_conn.select("INBOX")

    status, messages = imap_conn.search(None, "ALL")
    for message in messages[0].split():
        status, msg = imap_conn.fetch(message, "(RFC822)")
        for response_part in msg:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                print("=" * 100)
                print(f"Subject: {msg['Subject']}")
                print(f"From: {msg['From']}")
                print(f"Date: {msg['Date']}")

    imap_conn.close()
    imap_conn.logout()


def send_email():
    access_token = auth_device_flow()

    me_mail = os.getenv("OUTLOOK_USERNAME")

    msg = MIMEMultipart()
    msg["From"] = me_mail
    msg["To"] = os.getenv("OUTLOOK_TO")
    msg["Subject"] = "Meet for lunch?"
    msg.attach(
        MIMEText("Hey it's good to see you again. Let's meet for lunch today.", "plain")
    )

    smtp_conn = smtplib.SMTP(
        os.getenv("OUTLOOK_SMTP_SERVER"), os.getenv("OUTLOOK_SMTP_PORT")
    )
    smtp_conn.starttls()
    smtp_conn.ehlo()
    smtp_conn.auth(
        "XOAUTH2",
        lambda: f"user={me_mail}\1auth=Bearer {access_token}\1\1",
    )

    smtp_conn.send_message(msg)
    print(f"Email sent")

    smtp_conn.quit()


def main():
    # Follow the console info to login
    fetch_emails()
    send_email()


if __name__ == "__main__":
    main()
