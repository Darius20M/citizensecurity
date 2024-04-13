from django.conf import settings
from django.db import models
from django.utils import timezone

from security.utils.constants import DEVICE_TYPES


class SessionHistoryModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='session_histories', on_delete=models.PROTECT)
    token = models.CharField(max_length=600, db_index=True)
    last_activity = models.DateTimeField(default=timezone.now)
    previous_token = models.CharField(max_length=600, null=True, blank=True)
    expired = models.DateTimeField(default=timezone.now, null=False, blank=False)
    application = models.ForeignKey('security.ApplicationModel', related_name='session_histories', on_delete=models.PROTECT)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_offline = models.DateTimeField(default=timezone.now, blank=True, null=True)
    time_no_ready = models.FloatField(default=0, blank=True, null=True)
    offline = models.BooleanField(default=False)
    device = models.CharField(max_length=255, default='unknown')
    device_type = models.CharField(max_length=80, choices=DEVICE_TYPES, default=DEVICE_TYPES.unknown)
    browser = models.CharField(max_length=255, default='unknown')
    browser_version = models.CharField(max_length=80, default='unknown')
    system_operation = models.CharField(max_length=255, default='unknown')
    system_operation_version = models.CharField(max_length=80, default='unknown')
    created = models.DateTimeField(null=False, blank=False)
    modified = models.DateTimeField(null=False, blank=False)
    finalized = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'tsec_session_histories'
        verbose_name = 'Session'
        app_label = 'security'
        verbose_name_plural = 'Sessions'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(SessionHistoryModel, self).save(*args, **kwargs)
