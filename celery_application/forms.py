from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class PostForm(forms.Form):
    subject = forms.CharField(label='Name', max_length=30)
    email_recipient = forms.EmailField(label='Email', max_length=30)
    message = forms.CharField(label='Text', max_length=300)
    date_and_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M%S'],
        help_text='Year-month-day Hour:Min:Sec',
        initial=timezone.now()
    )

    def clean_date_and_time(self):
        data = self.cleaned_data['date_and_time']
        if not timezone.now() < data < timezone.now() + timedelta(days=2):
            raise ValidationError('Датавремя не может быть в прошлом, и не может быть более чем на 2 дня вперед.')
        return data


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=30)
    email = forms.EmailField(label='Email', max_length=30)
    message = forms.CharField(label='Сообщение', max_length=300)