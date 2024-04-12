from unittest import TestCase
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from rest_framework.views import APIView


class TestViews(APIView):

    def get_user_totp_device(self, user, confirmed=None):
        devices = devices_for_user(user, confirmed=confirmed)
        for device in devices:
            if isinstance(device, TOTPDevice):
                return device

    def create_device_topt_for_user(self, user):
        device = self.get_user_totp_device(user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        return device.generate_challenge()

    def validate_user_otp(self, user):
        device = self.create_device_topt_for_user(user)

    def post(self, request, *args, **kwargs):
        self.validate_user_otp(request.user)
