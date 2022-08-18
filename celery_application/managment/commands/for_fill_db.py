from celery_application.models import Author, Quotes
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Warning: use 1 time!'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, choices=range(1, 10000), help='Number of the creating values')

    def handle(self, *args, **options):
        number = options['number']
        authors = []
        quotes = []
        for i in range(number):
            author = Author(name=fake.name(),
                            description=fake.text())
            authors.append(author)
        Author.objects.bulk_create(authors)
        for i in range(number):
            quote = Quotes(message=fake.text(),
                           author_id=Author.objects.get(pk=i + 1).pk)
            quotes.append(quote)
        Quotes.objects.bulk_create(quotes)
        self.stdout.write(self.style.SUCCESS('Successfully! %s ' % number))
