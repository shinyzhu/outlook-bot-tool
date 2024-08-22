import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import httpx
import msal


def auth():
    client_id = os.getenv("OUTLOOK_CLIENT_ID")
    client_secret = os.getenv("OUTLOOK_CLIENT_SECRET")

    authority = f"https://login.microsoftonline.com/consumers"
    scopes = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        access_token = result["access_token"]
        print(result)
    else:
        print("Error acquiring token:", result.get("error_description"))

    return access_token


def receive_email():
    access_token = auth()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    response = httpx.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
    )

    if response.status_code == 200:
        emails = response.json()
        for email in emails["value"]:
            print(f"Subject: {email['subject']}")
    else:
        print("Error fetching emails:", response.text)


def send_email():
    access_token = auth()
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
        print("Email sent successfully!")
    else:
        print("Error sending email:", response.text)


def main():
    receive_email()
    send_email()


if __name__ == "__main__":
    main()
