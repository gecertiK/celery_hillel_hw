from django.urls import path

from celery_application.views import create_reminder, quote_list, AuthorDetailView, AuthorListView

app_name = 'reminder'
urlpatterns = [
    path('reminder/', create_reminder, name="create_reminder"),
    path('quotes/', quote_list, name='pagination_quotes'),
    path('authors/', AuthorListView.as_view(), name='pagination_authors'),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name='detail_author')
]
