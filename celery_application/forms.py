from django import forms


class ReminderForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    text = forms.CharField(max_length=255, required=True)
    datetime = forms.DateTimeField(help_text="Example: YYYY-MM-DD hh:mm: ss and not more than two days in advance!")
