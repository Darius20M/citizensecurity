from django.core.management import BaseCommand
from django.utils import timezone

from security.models import TwoFactorSettingsModel


class Command(BaseCommand):

    def handle(self, *args, **options):
        TwoFactorSettingsModel.objects.filter(
            otp_expiry__lt=timezone.now(),
            otp__isnull=False
        ).update(otp='', otp_expiry=None)
        self.stdout.write(
            self.style.SUCCESS('Successfully reset expired codes')
        )
