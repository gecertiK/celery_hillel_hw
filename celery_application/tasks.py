from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(text, email):
    send_mail("Reminder", text, 'admin@example.com', [email])
