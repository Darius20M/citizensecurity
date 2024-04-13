from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string


class TwoFactorSettingsModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='two_factor', on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    recovery_token = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=255, null=True, blank=True, default=None)
    token_expiry = models.DateTimeField(blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    failed_attempts = models.PositiveIntegerField(default=0)
    blocked_until = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)
    history = HistoricalRecords(table_name='tsec_hist_two_factor_settings')
    class Meta:
        db_table = 'tsec_two_factor_settings'
        app_label = 'security'
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TwoFactorSettingsModel, self).save(*args, **kwargs)

    def generate(self):
        if self.token_expiry is None or self.token_expiry < timezone.now():
            self.token = self.generate_token()
            self.token_expiry = timezone.now() + timedelta(hours=1)

        self.otp = self.generate_random_digits()
        self.otp_expiry = timezone.now() + timedelta(hours=1)
        self.save()

    def generate_random_digits(self, n=6):
        return "".join(map(str, random.sample(range(0, 10), n)))
    def generate_token(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(150))


    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.blocked_until = None
        self.save()

    def register_failed_attempt(self):
        self.failed_attempts += 1
        if self.failed_attempts >= settings.BRUTE_FORCE_THRESHOLD:
            self.blocked_until = timezone.now() + timedelta(seconds=settings.BRUTE_FORCE_TIMEOUT)
        self.save()

    def is_blocked(self):
        return self.blocked_until is not None and self.blocked_until > timezone.now()