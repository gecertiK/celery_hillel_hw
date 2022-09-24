from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .forms import ContactForm, PostForm
from .tasks import send_contact, send_task


def note_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email_recipient = form.cleaned_data['email_recipient']
            message = form.cleaned_data['message']
            deadline = form.cleaned_data['date_and_time']
            send_task.apply_async((subject, email_recipient, message), eta=deadline)
            return redirect('celery_form:index')
    else:
        form = PostForm()
    return render(
        request,
        'celery_form/index.html',
        {
            'note_form': form}
        )


def another_page(request):
    return render(request, 'celery_form/another_page.html')


def contact(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_contact.delay(name, email, message)
            data['form_is_valid'] = True
            msg = [f"Сообщение от {name} отправлено"]
            data['msg_list'] = render_to_string('celery_form/messages.html', {
                'messages': msg
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    return contact(request, form, 'celery_form/contact.html')