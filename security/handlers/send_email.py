from post_office import mail
from post_office.template import render_to_string
from django.conf import settings


def send_email(subject, html_path, context, obj):
    mail.send(
        recipients=[obj.user.email],
        context='This is an important message.',
        sender=settings.DEFAULT_FROM_EMAIL,
        subject=subject,
        html_message=render_to_string(html_path, context),
    )
