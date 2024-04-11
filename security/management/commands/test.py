from django.core.management import BaseCommand
from django.utils import timezone
from post_office import mail
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        print(settings.DEFAULT_FROM_EMAIL)
        mail.send(
            ['dariusjosedelacruz@gmail.com'],
            sender=settings.DEFAULT_FROM_EMAIL,
            subject='Welcome!',
            message='Welcome home, {{ name }}!',
            priority='now'
        )
