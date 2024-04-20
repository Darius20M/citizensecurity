from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from security.models.session_history_model import SessionHistoryModel
from security.utils.constants import DEVICE_TYPES


class SessionModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sessions', on_delete=models.PROTECT)
    token = models.CharField(max_length=600, db_index=True)
    last_activity = models.DateTimeField(default=timezone.now)
    previous_token = models.CharField(max_length=600, null=True, blank=True)
    expire = models.DateTimeField(default=timezone.now, null=False, blank=False)
    offline = models.BooleanField(default=False)
    last_offline = models.DateTimeField(default=timezone.now, blank=True, null=True)
    time_no_ready = models.FloatField(default=0, blank=True, null=True)
    application = models.ForeignKey('security.ApplicationModel', related_name='sessions', on_delete=models.PROTECT)
    ip_address = models.GenericIPAddressField(null=False, blank=False, default='127.0.0.1')
    device = models.CharField(max_length=255, default='unknown')
    device_type = models.CharField(max_length=80, choices=DEVICE_TYPES, default=DEVICE_TYPES.unknown)
    browser = models.CharField(max_length=255, default='unknown', null=False, blank=False)
    browser_version = models.CharField(max_length=80, default='unknown')
    system_operation = models.CharField(max_length=255, default='unknown')
    system_operation_version = models.CharField(max_length=80, default='unknown')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = _('tsec_sessions')
        app_label = 'security'
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        unique_together = ('user', 'ip_address', 'application',)

    def expired(self):
        return self.expire >= timezone.now()

    def close_session(self):

        self.offline = True
        self.save()

        if not SessionHistoryModel.objects.filter(id=self.id).exists():
            session_history = SessionHistoryModel()
            session_history.id = self.id
            session_history.device = self.device
            session_history.created = self.created
            session_history.modified = self.modified
            session_history.application = self.application
            session_history.user = self.user
            session_history.browser = self.browser
            session_history.offline = self.offline
            session_history.expire = self.expire
            session_history.browser_version = self.browser_version
            session_history.device_type = self.device_type
            session_history.token = self.token
            session_history.system_operation = self.system_operation
            session_history.system_operation_version = self.system_operation_version
            session_history.ip_address = self.ip_address
            session_history.previous_token = self.previous_token
            session_history.last_offline = self.last_offline
            session_history.time_no_ready = self.time_no_ready
            session_history.last_activity = self.last_activity
            session_history.finalized = timezone.now()
            session_history.save()

        self.delete()

    def save(self, *args, **kwargs):
        if self.id is None:
            self.created = timezone.now()

        if self.token is not None:
            self.previous_token = self.token

        if self.offline is None or self.offline:
            self.last_offline = timezone.now()
        elif not self.offline:
            if self.last_offline is not None:
                self.time_no_ready = (timezone.now() - self.last_offline).total_seconds()

        self.modified = timezone.now()
        return super(SessionModel, self).save(*args, **kwargs)

    def fullname(self):
        user = self.user
        if user.last_name is not None:
            return user.first_name + ' ' + user.last_name
        else:
            return user.first_name

    def __str__(self):
        return "Session id => %d User => %s" % (self.id, self.user.username)