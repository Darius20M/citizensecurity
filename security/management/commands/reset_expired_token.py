from django.core.management import BaseCommand
from django.utils import timezone

from security.models import TwoFactorSettingsModel


class Command(BaseCommand):

    def handle(self, *args, **options):
        TwoFactorSettingsModel.objects.filter(
            token_expiry__lt=timezone.now(),
            token__isnull=False
        ).update(token='', token_expiry=None)
        self.stdout.write(
            self.style.SUCCESS('Successfully reset expired token')
        )
