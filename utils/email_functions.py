from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email(subject,body,to):
    print(subject,body,to)
    email = EmailMessage(
        subject,
        body,
        'Dont Reply <do_not_reply@domain.com>',
        [to]
    )
    email.content_subtype = 'html'
    print(email.send())