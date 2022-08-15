from celery import shared_task
from django.core.mail import send_mail
from bs4 import BeautifulSoup
from celery_application.models import Author, Quotes
import requests


@shared_task
def send_email(text, email):
    send_mail("Reminder", text, 'admin@example.com', [email])


@shared_task
def work_done():
    send_mail(
        subject='Work has ended',
        message='No more quotes',
        from_email='david@example.com',
        recipient_list=['admin@example.com', ],
        fail_silently=False
    )


@shared_task
def parse_quotes():
    count = 0
    url = 'https://quotes.toscrape.com/'
    quote_list = []
    while count < 5:
        get_url = requests.get(url)
        beautifulsoup_html = BeautifulSoup(get_url.content, 'html.parser')
        quote_db = Quotes.objects.values('texts')
        quotes = beautifulsoup_html.find_all("div", {"class": "quote"})
        for _ in quote_db:
            quote_list.append(['texts'])
        for get_quote in quotes:
            if get_quote.span.text not in quote_list:
                authors = get_quote.small.text
                url_description = requests.get(url + get_quote.a.get('href'))
                soup_description = BeautifulSoup(url_description.content, 'html.parser')
                auth_description = soup_description.find("div", {"class": "author-description"})
                author = Author.objects.get_or_create(name=authors, defaults={'description': auth_description.text})
                Quotes.objects.get_or_create(message=get_quote.span.text, author=author[0])
                count += 1
                if count == 5:
                    break
            if get_quote.span.text or count < 5 not in quote_list:
                next_page = beautifulsoup_html.find("li", {"class": "next"}).a.get("href")
                url = url + next_page
            else:
                url = None
                work_done.delay()
