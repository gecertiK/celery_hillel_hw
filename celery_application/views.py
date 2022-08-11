import datetime
from django.shortcuts import render
from django.utils import timezone
from celery_application.forms import ReminderForm
from celery_application.tasks import send_email


def create_reminder(request):
    if request.method == 'POST':
        reminder_form = ReminderForm(request.POST)
        if reminder_form.is_valid():
            email = reminder_form.cleaned_data['email']
            text = reminder_form.cleaned_data['text']
            data = reminder_form.cleaned_data['datetime']
            today_now = timezone.now()
            if today_now < data < today_now + datetime.timedelta(days=2):
                message = "Message was sent successfully!"
                send_email.apply_async((text, email), eta=data)
                return render(
                    request,
                    'celery_application/send_email.html',
                    {'reminder_form': reminder_form, 'message': message, })
            else:
                message = "Please chose the correct date"
                return render(
                    request,
                    'celery_application/send_email.html',
                    {'reminder_form': reminder_form, 'message': message, })
    else:
        reminder_form = ReminderForm()
    return render(request, 'celery_application/send_email.html', {'reminder_form': reminder_form, })
