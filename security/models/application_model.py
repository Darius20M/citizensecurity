import hashlib
import hmac
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from security.managers.application_manager import ApplicationManager


"""def path_file(self, filename):
    return "security/applications/%s/%s" % (self.user.username, filename)"""


class ApplicationModel(models.Model):
    name = models.CharField(max_length=80, unique=True, null=False, blank=False)
    code = models.CharField(max_length=30, null=False, blank=False, default='APP')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='application', on_delete=models.PROTECT)
    key = models.CharField(max_length=128, blank=True, default='', db_index=True)
    secret = models.CharField(max_length=128, blank=True, default='', db_index=True)
    two_factor_enabled = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)
    parent = models.ForeignKey('self', related_name='child', null=True, blank=True, on_delete=models.PROTECT,
                               default=None)
    #logo = models.FileField(upload_to=path_file, default=None)
    about = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='application_created', on_delete=models.PROTECT)
    modified = models.DateTimeField(default=timezone.now, editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='application_modified', on_delete=models.PROTECT)
    history = HistoricalRecords(table_name='tsec_hist_application')

    objects = ApplicationManager()

    class Meta:
        db_table = 'tsec_applications'
        app_label = 'security'

    def generate_key(self):
        # obtiene random UUID
        new_uuid = uuid.uuid4()
        # Hmac that beast
        return hmac.new(new_uuid.bytes, digestmod=hashlib.sha1).hexdigest()

    def generate_secret(self):
        # Obtiene random UUID
        new_uuid = uuid.uuid4()

        raw = settings.SECRET_KEY.encode('utf-8')
        # Hmac that beast
        return hmac.new(new_uuid.bytes, msg=raw, digestmod=hashlib.sha1).hexdigest()

    def update_tokens(self):
        self.key = self.generate_key()
        self.secret = self.generate_secret()
        self.save()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        if not self.secret:
            self.secret = self.generate_secret()

        if not self.id:
            self.created = timezone.now()

        self.modified = timezone.now()

        return super(ApplicationModel, self).save(*args, **kwargs)

    def isStaff(self):
        return self.is_staff

