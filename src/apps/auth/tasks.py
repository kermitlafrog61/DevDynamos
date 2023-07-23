import smtplib
from email.message import EmailMessage

from core.celery import app


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def verification_code(user_email: str, code: str):
    from core.settings import settings
    message = EmailMessage()
    message["Subject"] = "Account verification"
    message["From"] = settings.EMAIL_HOST
    message["To"] = user_email

    message.set_content(
        f"Here is your code: {code}\nEnter verification code on this link: http://127.0.0.1:8000/docs#/Auth/profile_activation_api_v1_auth_confirm_post"
    )
    return message


@app.task
def send_email_confirmation(user_email: str, code: str):
    from core.settings import settings
    message = verification_code(user_email=user_email, code=code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(settings.EMAIL_HOST, settings.EMAIL_PASSWORD)
        server.send_message(message)


def recovery_code(user_email: str, code: str):
    from core.settings import settings
    message = EmailMessage()
    message["Subject"] = "Account recovery"
    message["From"] = settings.EMAIL_HOST
    message["To"] = user_email

    message.set_content(
        f"Here is your code: {code}\nEnter recovery code on this link: http://127.0.0.1:8000/docs#/Auth/profile_set_new_password_api_v1_auth_password_recovery_post"
    )
    return message


@app.task
def send_email_recovery(user_email: str, code: str):
    from core.settings import settings
    message = recovery_code(user_email=user_email, code=code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(settings.EMAIL_HOST, settings.EMAIL_PASSWORD)
        server.send_message(message)
