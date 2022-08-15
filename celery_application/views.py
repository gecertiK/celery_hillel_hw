from django.shortcuts import render
from celery_application.forms import ReminderForm
from celery_application.tasks import send_email


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
