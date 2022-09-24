from django.urls import path

from .views import another_page, contact_form, note_form


app_name = 'celery_form'
urlpatterns = [
    path('', note_form, name='index'),
    path('contact/', contact_form, name='contact'),
    path('another_page/', another_page, name='another_page')
]