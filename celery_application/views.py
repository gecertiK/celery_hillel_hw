from django.http import Http404
from django.shortcuts import render
from django.views import generic

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from celery_application.forms import ReminderForm
from celery_application.models import Author, Quotes
from celery_application.tasks import send_email
from django.views.decorators.cache import cache_page


def create_reminder(request):
    if request.method == 'POST':
        reminder_form = ReminderForm(request.POST)
        if reminder_form.is_valid():
            email = reminder_form.cleaned_data['email']
            text = reminder_form.cleaned_data['text']
            data = reminder_form.cleaned_data['datetime']
            message = "Message was sent!"
            send_email.apply_async((text, email), eta=data)
            return render(
                request,
                'celery_application/send_email.html',
                {'reminder_form': reminder_form, 'message': message, })
    else:
        reminder_form = ReminderForm()
    return render(
        request,
        'celery_application/send_email.html',
        {'reminder_form': reminder_form, })


@cache_page(1)
def quote_list(request):
    quotes_list = Quotes.objects.select_related('author').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(quotes_list, 150)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        raise Http404
    context = {'page_obj': page_obj}
    return render(request, 'celery_application/pagination_quotes.html', context)


class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()
    paginate_by = 200
    template_name = 'celery_application/pagination_authors.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'celery_application/detail_author.html'
