import os

from dotenv import load_dotenv

load_dotenv()

import logging

logging.basicConfig(level=logging.INFO)

import httpx
import msal

import imaplib, smtplib, email
from email.header import decode_header

from file_token_cache import FileTokenCache
from outlook_auth import auth_device_flow


def decode_str(string):
    decoded, encoding = decode_header(string)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or "utf-8")
    return decoded


# see: https://blog.bytescrum.com/how-to-get-and-send-email-in-python-using-imap-and-smtp
def fetch_emails_and_attachments():
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


def send_email():
    access_token = auth_device_flow()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    email_data = {
        "message": {
            "subject": "Test Email Again",
            "body": {"contentType": "Text", "content": "This is a test email."},
            "toRecipients": [{"emailAddress": {"address": "shiny@shinyzhu.com"}}],
        }
    }

    response = httpx.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json=email_data,
    )

    if response.status_code == 202:
        print("📧 Email sent successfully!")
    else:
        print("❌ Error sending email:", response.text)


def main():
    fetch_emails_and_attachments()


# send_email()


if __name__ == "__main__":
    main()
