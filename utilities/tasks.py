from celery import shared_task
from django.core.mail import send_mail


import os

from dotenv import load_dotenv


load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_HOST_USER")


@shared_task(queue="billr")
def send_email(subject,body,recipients,from_email=EMAIL_SENDER):
    send_mail(subject=subject,message=body,from_email=from_email,recipient_list=recipients)
