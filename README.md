# Outlook Mailbot Tool

To fetch and send emails with a **personal** `@outlook.com` account in a Python CLI app.

This project is introducing how to use the [Modern Authentication](https://support.microsoft.com/en-us/office/modern-authentication-methods-now-needed-to-continue-syncing-outlook-email-in-non-microsoft-email-apps-c5d65390-9676-4763-b41f-d7986499a90d) rather than username/password. And the `msal`, `imaplib` and `smtplib` that you're familiar with.

## Create a new Python env with conda

```sh
conda create -n ohoutlook python-dotenv msal
conda activate ohoutlook
```

## Register an Entra App

