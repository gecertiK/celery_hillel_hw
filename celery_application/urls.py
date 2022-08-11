from django.urls import path

from celery_application.views import create_reminder

app_name = 'reminder'
urlpatterns = [
    path('', create_reminder, name="create_reminder"),
    ]
