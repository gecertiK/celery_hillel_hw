import re
from datetime import date, datetime

from bs4 import BeautifulSoup

from celery import shared_task

from django.core.mail import send_mail

import requests

from .models import Author, Quote


@shared_task
def send_task(subject, email_recipient, message):
    send_mail(
        subject=subject,
        message=message,
        from_email='admin@example.com',
        recipient_list=[email_recipient],
        fail_silently=False
    )


@shared_task
def send_contact(subject, email, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=email,
        recipient_list=['admin@example.com'],
        fail_silently=False
    )


@shared_task
def email_done():
    send_mail(
        subject='Job is done',
        message='All ok',
        from_email='admin@example.com',
        recipient_list=['admin@example.com', ],
        fail_silently=False
    )


@shared_task
def parse_quote():
    base_url = 'http://quotes.toscrape.com'
    pattern = r"\b([a-zA-Z]+)\s(\d+),\s(\d+)\b"
    page_url = '/page/1'
    count = 0

    while page_url:
        res = requests.get(base_url + page_url)
        html = BeautifulSoup(res.content, 'html.parser')

        quotes = html.find_all('div', {'class': 'quote'})

        for quote in quotes:
            if Quote.objects.filter(text=quote.span.text).exists():
                continue

            auth_request = requests.get(base_url + quote.a.get('href'))
            auth_html = BeautifulSoup(auth_request.content, 'html.parser')
            auth_desc = auth_html.find('div', {'class': 'author-description'}).text.strip()
            birth_day = re.search(pattern, auth_html.text)
            auth_obj, created = Author.objects.get_or_create(
                name=quote.small.text,
                defaults={
                    'birthday':
                        date(int(birth_day[3]),
                             datetime.strptime(birth_day[1], '%B').month,
                             int(birth_day[2])),
                    'description': auth_desc,
                },
            )

            Quote.objects.create(
                text=quote.span.text,
                author=auth_obj
            )
            count += 1
            if count == 5:
                return

        if count < 5:
            next_btn = html.find('li', {'class': 'next'})
            if next_btn:
                page_url = next_btn.a.get('href')
            else:
                page_url = None
                email_done.delay()